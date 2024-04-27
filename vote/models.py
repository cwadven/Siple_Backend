from django.db import models
from vote.consts import (
    VoteAnswerReferencePKTypes,
    VoteRewardAppliedStatus,
    VoteRewardStorageType,
    VoteRewardTargetType,
    VoteStatus,
)


class Vote(models.Model):
    vote_ref_pk = models.CharField(
        max_length=100,
        verbose_name='Vote Reference Primary Key',
        db_index=True,
    )
    vote_ref_pk_type = models.CharField(
        max_length=100,
        verbose_name='Vote Type',
        db_index=True,
    )
    type = models.CharField(
        max_length=100,
        verbose_name='Vote Reason for Type',
        db_index=True,
    )
    start_at = models.DateTimeField(
        verbose_name='Vote Start Date',
        db_index=True,
    )
    end_at = models.DateTimeField(
        verbose_name='Vote End Date',
        db_index=True,
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Vote Title',
    )
    description = models.TextField(
        verbose_name='Vote Description',
    )
    status = models.CharField(
        max_length=100,
        verbose_name='Vote Status',
        choices=VoteStatus.choices(),
    )
    need_to_finish_vote_number = models.IntegerField(
        verbose_name='Need to Finish Vote Number',
        default=0,
    )
    current_finish_vote_number = models.IntegerField(
        verbose_name='Current Finish Vote Number',
        default=0,
    )
    is_multiple_selection = models.BooleanField(
        verbose_name='Multiple Selection',
        default=False,
    )
    is_deleted = models.BooleanField(
        verbose_name='Vote Deleted',
        default=False,
    )
    deleted_at = models.DateTimeField(
        verbose_name='Vote Deleted Date',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '투표'
        verbose_name_plural = '투표'

    def __str__(self):
        return self.title


class VotingRecord(models.Model):
    vote = models.ForeignKey(
        Vote,
        on_delete=models.DO_NOTHING,
    )
    member = models.ForeignKey(
        'member.Member',
        on_delete=models.DO_NOTHING,
    )
    is_answered = models.BooleanField(
        default=False,
    )
    additional_message = models.TextField(
        null=True,
        blank=True,
    )
    answered_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '투표지'
        verbose_name_plural = '투표지'

    def __str__(self):
        return f'{self.vote_id} - {self.member_id}'


class VotingAnswer(models.Model):
    voting_record = models.ForeignKey(
        VotingRecord,
        on_delete=models.DO_NOTHING,
    )
    answer_ref_pk = models.CharField(
        max_length=100,
        verbose_name='Voting Answer Reference Primary Key',
        db_index=True,
    )
    answer_ref_pk_type = models.CharField(
        max_length=100,
        verbose_name='Voting Answer Reference PK Type',
        choices=VoteAnswerReferencePKTypes.choices(),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '투표지의 투표 답변'
        verbose_name_plural = '투표지의 투표 답변'

    def __str__(self):
        return f'{self.voting_record_id} - {self.answer_ref_pk_type} - {self.answer_ref_pk}'


class VotingDefaultSelection(models.Model):
    type = models.CharField(
        max_length=100,
        verbose_name='Vote Default Selection Type',
        db_index=True,
    )
    display_name = models.CharField(
        max_length=100,
        verbose_name='Vote Default Selection Displaying Name',
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Vote Default Selection Name',
        db_index=True,
    )
    description = models.TextField(
        verbose_name='Vote Default Selection Description',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '투표 기본 답변'
        verbose_name_plural = '투표 기본 답변'

    def __str__(self):
        return f'{self.type} - {self.display_name} {self.name}'


class VoteRewardStorage(models.Model):
    vote = models.ForeignKey(
        Vote,
        on_delete=models.DO_NOTHING,
    )
    reward_ref_pk = models.CharField(
        max_length=100,
        verbose_name='Reward Reference Primary Key',
        db_index=True,
        null=True,
        blank=True,
    )
    reward_ref_pk_type = models.CharField(
        max_length=100,
        verbose_name='Reward Reference Primary Key Type',
        choices=VoteRewardStorageType.choices(),
        null=True,
        blank=True,
    )
    reward_applied_status = models.CharField(
        max_length=100,
        verbose_name='Vote Reward Applied Status',
        choices=VoteRewardAppliedStatus.choices(),
    )
    applied_at = models.DateTimeField(
        verbose_name='Vote Reward Applied Date',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '투표 보상 저장소'
        verbose_name_plural = '투표 보상 저장소'

    def __str__(self):
        return f'{self.vote_id} - {self.reward_ref_pk} - {self.reward_ref_pk_type}'


class VoteRewardTarget(models.Model):
    vote_reward_storage = models.ForeignKey(
        VoteRewardStorage,
        on_delete=models.DO_NOTHING,
    )
    reward_target_pk = models.CharField(
        max_length=100,
        verbose_name='Reward Target Primary Key',
        db_index=True,
    )
    reward_target_pk_type = models.CharField(
        max_length=100,
        verbose_name='Reward Target Primary Key Type',
        choices=VoteRewardTargetType.choices(),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '투표 보상 대상'
        verbose_name_plural = '투표 보상 대상'

    def __str__(self):
        return f'{self.reward_target_pk} - {self.reward_target_pk_type}'
