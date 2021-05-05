import datetime

from django.db.models import Q

import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import Diary


class DiaryType(DjangoObjectType):

    class Meta:
        model = Diary
        # fields = ("id", "title", "entry")
        fields = "__all__"


class CreateEntry(graphene.Mutation):

    class Arguments:
        entry_title = graphene.String(required=True)
        entry_body = graphene.String(required=True)

    # Note:: This defines the response of the mutation
    diary_entry = graphene.Field(DiaryType)

    @classmethod
    @login_required
    def mutate(cls, root, info, entry_title, entry_body):
        user = info.context.user
        print(user)

        # if user.is_anonymous:
        #     raise Exception('Authentication Failure: Your must be signed in')

        # FIXME access entry
        diary_entry = Diary(title=entry_title, entry=entry_body)
        diary_entry.save()

        return CreateEntry(diary_entry=diary_entry)


class EntryMutation(graphene.Mutation):

    class Arguments:
        entry_id = graphene.String(required=True)
        changed_entry_title = graphene.String(required=True)
        entry_body = graphene.String(required=True)

    # Note:: This defines the response of the mutation
    diary_entry = graphene.Field(DiaryType)

    @classmethod
    @login_required
    def mutate(cls, root, info, entry_id, entry_body=None, changed_entry_title=None):
        diary_entry = Diary.objects.get(entry_id=entry_id)

        diary_entry.entry = entry_body if entry_body is not None and entry_body != "" else diary_entry.entry
        diary_entry.title = changed_entry_title if changed_entry_title is not None and changed_entry_title != "" else diary_entry.title

        diary_entry.save()

        return EntryMutation(diary_entry=diary_entry)


class DeleteEntry(graphene.Mutation):

    class Arguments:
        entry_id = graphene.String(required=True)

    # Note:: This defines the response of the mutation
    diary_entry = graphene.Field(DiaryType)

    @classmethod
    @login_required
    def mutate(cls, root, info, entry_id):
        user = info.context.user
        diary_entry = Diary.objects.get(entry_id=entry_id)

        diary_entry.delete()

        return DeleteEntry(diary_entry=diary_entry)


class Query(graphene.ObjectType):

    # Get all Entries
    diary_entries = graphene.List(DiaryType, name="allEntries")

    def resolve_diary_entries(root, info):
        return Diary.objects.all()

    # get entries by ID
    entry_by_id = graphene.Field(
        DiaryType, entry_no=graphene.String(required=True), name="entryID"
    )

    def resolve_entry_by_id(root, info, entry_no):

        # Querying a single entry
        return Diary.objects.get(entry_no=entry_no)

    # Search Entries by Title
    entry_by_title = graphene.Field(
        DiaryType, search=graphene.String(required=True), name="entryTitle"
    )

    def resolve_entry_by_title(root, info, search):

        filter = (Q(title__icontains=search))
        return Diary.objects.filter(filter)

    # Filter entries by Date created
    entry_by_date_created = graphene.Field(
        DiaryType,
        date=graphene.DateTime(required=True),
        name="entryDate"
    )

    def resolve_entry_by_date_created(root, info, date):
        return Diary.objects.filter(created_on=date)

    # Filter entries by Date Modified Range
    entry_by_date_modified = graphene.Field(
        DiaryType,
        start=graphene.DateTime(required=True),
        end=graphene.DateTime(required=True),
        name="modifyRange"
    )

    def resolve_entry_by_date_modified(root, info, start, end):
        end = end + datetime.timedelta(days=1)
        return Diary.objects.filter(modified_at__range=(start, end))


class Mutation(graphene.ObjectType):

    create_entry = CreateEntry.Field()
    update_entry = EntryMutation.Field()
    delete_entry = DeleteEntry.Field()
