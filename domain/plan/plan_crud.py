from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from models import Plan, User
from domain.plan.plan_schema import PlanCreate, PlanUpdate

from datetime import datetime


def get_plan_list(db: Session, skip: int = 0, limit: int = 10,
                  keyword: str = None):
    stmt = select(Plan)

    if keyword:
        keyword = f"%{keyword}%"
        stmt = (stmt
                # .outerjoin(User, Plan.owner_id == User.id)
                .filter(
                    Plan.title.ilike(keyword) |
                    Plan.content.ilike(keyword) |
                    Plan.topic.ilike(keyword)
                ))
        
    total = db.execute(select(func.count())
                       .select_from(stmt.distinct())).scalar()

    plan_list = db.execute(stmt.order_by(Plan.create_date.desc())
                           .offset(skip)
                           .limit(limit)).scalars().all()
    
    return total, plan_list

def get_plan(db: Session, plan_id: int):
    plan = db.query(Plan).get(plan_id)
    return plan

def get_max_plan_id(db: Session):
    id = db.execute(
        select(func.max(Plan.id)).select_from(Plan).limit(1)
        ).scalars().first()
    return id

def create_plan(db: Session, plan_create: PlanCreate, user: User):
    db_plan = Plan(title = plan_create.title,
                   content = plan_create.content,
                   goal = plan_create.goal,
                   nuri = plan_create.nuri,
                   topic = plan_create.topic,
                   activity = plan_create.activity,
                   create_date = datetime.now(),
                   owner = user)
    db.add(db_plan)
    db.commit()

def update_plan(db: Session, db_plan: Plan,
                plan_update: PlanUpdate):
    db_plan.title = plan_update.title
    db_plan.content = plan_update.content
    db_plan.goal = plan_update.goal
    db_plan.nuri = plan_update.nuri
    db_plan.topic = plan_update.topic
    db_plan.activity = plan_update.activity
    if plan_update.modify_date:
        db_plan.modify_date = plan_update.modify_date
    else:
        db_plan.modify_date = datetime.now()
    db.add(db_plan)
    db.commit()

def delete_plan(db: Session, db_plan: Plan):
    db.delete(db_plan)
    db.commit()