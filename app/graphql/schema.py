import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.modules.api.models import API as APIModel
from app.modules.issue.models import Issue as IssueModel
from app.core.db import SessionLocal

class APIType(SQLAlchemyObjectType):
    class Meta:
        model = APIModel
        interfaces = (graphene.relay.Node,)

class IssueType(SQLAlchemyObjectType):
    class Meta:
        model = IssueModel
        interfaces = (graphene.relay.Node,)

class Query(graphene.ObjectType):
    all_apis = graphene.List(APIType, include_issues=graphene.Boolean(default_value=False))
    all_issues = graphene.List(IssueType)

    def resolve_all_apis(self, info, include_issues):
        db = SessionLocal()
        query = db.query(APIModel)
        if include_issues:
            from sqlalchemy.orm import joinedload
            query = query.options(joinedload(APIModel.issues))
        return query.all()

    def resolve_all_issues(self, info):
        db = SessionLocal()
        return db.query(IssueModel).all()

class CreateAPI(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    api = graphene.Field(lambda: APIType)

    def mutate(self, info, name, description=None):
        db = SessionLocal()
        api = APIModel(name=name, description=description)
        db.add(api)
        db.commit()
        db.refresh(api)
        return CreateAPI(api=api)

class UpdateAPI(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()

    api = graphene.Field(lambda: APIType)

    def mutate(self, info, id, name=None, description=None):
        db = SessionLocal()
        api = db.query(APIModel).filter(APIModel.id == id).first()
        if not api:
            raise Exception("API not found")
        if name:
            api.name = name
        if description:
            api.description = description
        db.commit()
        db.refresh(api)
        return UpdateAPI(api=api)

class DeleteAPI(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    ok = graphene.Boolean()

    def mutate(self, info, id):
        db = SessionLocal()
        api = db.query(APIModel).filter(APIModel.id == id).first()
        if not api:
            return DeleteAPI(ok=False)
        db.delete(api)
        db.commit()
        return DeleteAPI(ok=True)

class CreateIssue(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()

    issue = graphene.Field(lambda: IssueType)

    def mutate(self, info, title, description=None):
        db = SessionLocal()
        issue = IssueModel(title=title, description=description)
        db.add(issue)
        db.commit()
        db.refresh(issue)
        return CreateIssue(issue=issue)

class UpdateIssue(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()

    issue = graphene.Field(lambda: IssueType)

    def mutate(self, info, id, title=None, description=None):
        db = SessionLocal()
        issue = db.query(IssueModel).filter(IssueModel.id == id).first()
        if not issue:
            raise Exception("Issue not found")
        if title:
            issue.title = title
        if description:
            issue.description = description
        db.commit()
        db.refresh(issue)
        return UpdateIssue(issue=issue)

class DeleteIssue(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    ok = graphene.Boolean()

    def mutate(self, info, id):
        db = SessionLocal()
        issue = db.query(IssueModel).filter(IssueModel.id == id).first()
        if not issue:
            return DeleteIssue(ok=False)
        db.delete(issue)
        db.commit()
        return DeleteIssue(ok=True)

class AddIssueToAPI(graphene.Mutation):
    class Arguments:
        api_id = graphene.Int(required=True)
        issue_id = graphene.Int(required=True)
    api = graphene.Field(lambda: APIType)

    def mutate(self, info, api_id, issue_id):
        db = SessionLocal()
        api = db.query(APIModel).filter(APIModel.id == api_id).first()
        issue = db.query(IssueModel).filter(IssueModel.id == issue_id).first()
        if not api or not issue:
            raise Exception("API or Issue not found")
        if issue not in api.issues:
            api.issues.append(issue)
            db.commit()
            db.refresh(api)
        return AddIssueToAPI(api=api)

class RemoveIssueFromAPI(graphene.Mutation):
    class Arguments:
        api_id = graphene.Int(required=True)
        issue_id = graphene.Int(required=True)
    api = graphene.Field(lambda: APIType)

    def mutate(self, info, api_id, issue_id):
        db = SessionLocal()
        api = db.query(APIModel).filter(APIModel.id == api_id).first()
        issue = db.query(IssueModel).filter(IssueModel.id == issue_id).first()
        if not api or not issue:
            raise Exception("API or Issue not found")
        if issue in api.issues:
            api.issues.remove(issue)
            db.commit()
            db.refresh(api)
        return RemoveIssueFromAPI(api=api)

class Mutation(graphene.ObjectType):
    create_api = CreateAPI.Field()
    update_api = UpdateAPI.Field()
    delete_api = DeleteAPI.Field()
    create_issue = CreateIssue.Field()
    update_issue = UpdateIssue.Field()
    delete_issue = DeleteIssue.Field()
    add_issue_to_api = AddIssueToAPI.Field()
    remove_issue_from_api = RemoveIssueFromAPI.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
