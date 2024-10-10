from datetime import date, datetime
from uuid import UUID
from ninja import Schema


################
# MODEL SCHEMAS
################
class UserRegisterIn(Schema):
    username: str
    email: str
    password: str
    role: str

class UserSignIn(Schema):
    username: str
    email: str
    password: str

class PasswordUpdate(Schema):
    email: str
    password: str
    new_password: str

class UserIn(Schema):
    uid: str
    first_name: str
    last_name: str
    username: str
    email: str
    street: str
    street_2: str
    city: str
    province: str
    country: str
    country_code: str
    postal_code: str
    gender: str
    role: str
    cell_number: str
    work_number: str
    home_number: str
    pin_code: str
    password: str
    notes: str
    last_logged_in: datetime
    password_changed_at: datetime
    date_joined: date
    active: bool
    archived: bool
    confirm_email: bool
    pending_approval: bool
    date_of_birth: date

class UserOutFull(Schema):
    id: UUID
    uid: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    street: str
    street_2: str
    city: str
    province: str
    country: str
    country_code: str
    postal_code: str
    gender: str
    role: str
    cell_number: str
    work_number: str
    home_number: str
    pin_code: str
    password: str
    notes: str
    last_logged_in: datetime
    password_changed_at: datetime
    date_joined: date
    active: bool
    archived: bool
    confirm_email: bool
    pending_approval: bool
    date_of_birth: date

class UserOut(Schema):
    id: UUID
    uid: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    active: bool
    archived: bool
    confirm_email: bool
    role: str