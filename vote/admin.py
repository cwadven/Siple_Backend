from django.contrib import admin
from vote.models import (
    Vote,
    VoteRewardStorage,
    VoteRewardTarget,
    VotingAnswer,
    VotingDefaultSelection,
    VotingRecord,
)


class VoteAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'vote_ref_pk',
        'vote_ref_pk_type',
        'type',
        'start_at',
        'end_at',
        'title',
        'need_to_finish_vote_number',
        'current_finish_vote_number',
    ]


class VoteRewardStorageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'vote_id',
        'reward_ref_pk',
        'reward_ref_pk_type',
        'reward_applied_status',
        'applied_at',
    ]


class VoteRewardTargetAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'vote_reward_storage_id',
        'reward_target_pk',
        'reward_target_pk_type',
    ]


class VotingRecordAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'vote_id',
        'member_id',
        'is_answered',
    ]


class VotingAnswerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'voting_record_id',
        'answer_ref_pk',
        'answer_ref_pk_type',
    ]


class VotingDefaultSelectionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'type',
        'display_name',
        'name',
    ]


admin.site.register(Vote, VoteAdmin)
admin.site.register(VoteRewardStorage, VoteRewardStorageAdmin)
admin.site.register(VoteRewardTarget, VoteRewardTargetAdmin)
admin.site.register(VotingRecord, VotingRecordAdmin)
admin.site.register(VotingAnswer, VotingAnswerAdmin)
admin.site.register(VotingDefaultSelection, VotingDefaultSelectionAdmin)
