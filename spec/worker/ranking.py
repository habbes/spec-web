
import math
from django.contrib.auth.models import User
from social.apps.django_app.default.models import UserSocialAuth
from django.db.models import ObjectDoesNotExist
from github import Github
from main.models import Skill, Profile, ProfileSkill, RankingResults


class ProfileRanker:
    def __init__(self, user):
        self.user = user
        self.score = 0
        provider = 'github'
        self.social = UserSocialAuth.objects.get(provider=provider, user_id = user.id)
        self.profile = user.profile
        self.token = self.social.extra_data['access_token']
        self.github = Github(login_or_token=self.token)
        self.github_user = self.github.get_user()
        self.repos = self.github_user.get_repos()

    def compute_score(self):
        print('Compute score of user', self.user)
        # init scores to 0
        self.score = 0
        for ps in self.profile.profileskill_set.all():
            ps.skill_score = 0
            ps.save()

        for repo in self.repos:
            pscore = self.project_score(repo)
            self.score += pscore
            self.skills_score(repo, pscore)
        self.profile.overall_score = self.score
        self.profile.save()

    def project_score(self, repo):
        print('Compute project score', repo.name)
        score = 0
        score = repo.forks_count**2 + repo.stargazers_count**2 + repo.size**2
        score = math.sqrt(score)
        weight = self.compute_project_weight(repo)
        return score * weight

    def skills_score(self, repo, repo_score):
        langs = repo.get_languages()
        lang_names = langs.keys()
        lang_contribs = langs.values()
        lang_contrib_total = sum(lang_contribs)
        for lang, contrib in zip(lang_names, lang_contribs):
            print('Compute skill score', lang)
            try:
                skill = Skill.objects.get(name=lang)
            except ObjectDoesNotExist as e:
                continue
            ps = ProfileSkill.objects.get(skill=skill, profile=self.profile)
            skill_score = repo_score * (contrib/lang_contrib_total)
            ps.skill_score += skill_score
            # update skill score upper bound
            if ps.skill_score > skill.max_score:
                skill.max_score = ps.skill_score
                skill.save()
            ps.save()

    def compute_project_weight(self, repo):
        return 0 if repo.fork else 1


def rank_profiles():
    users = User.objects.all()
    max_score = 0
    sum_score = 0
    for user in users:
        ranker = ProfileRanker(user)
        ranker.compute_score()
        if ranker.score > max_score:
            max_score = ranker.score
        sum_score += ranker.score
    average = sum_score / len(users)
    results = RankingResults.objects.create(max_score=max_score, average_score=average)
    print('Normalize profile scores scores')
    for profile in Profile.objects.all():
        score = profile.overall_score / max_score
        #dampen score to avoid perfect scores
        score = score * 0.89
        profile.normalized_score = score
        profile.save()

    print('Normalie skill scores')
    skills = Skill.objects.all()
    for skill in skills:
        max_score = skill.max_score
        sum_score = 0
        pskills = skill.profileskill_set.all()
        if max_score > 0:
            for ps in pskills:
                sum_score += ps.skill_score
                score = ps.skill_score/max_score
                score = score * 0.89
                ps.normalized_skill_score = score
                ps.save()
        average = sum_score / len(pskills)
        skill.average_score = average
        skill.save()
    return results
