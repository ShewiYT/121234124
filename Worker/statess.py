from aiogram.dispatcher.filters.state import State, StatesGroup

class NewUserForm(StatesGroup):
    time = State()
    info = State()
    experience = State()

class Report(StatesGroup):
    q1 = State()

class BanReport(StatesGroup):
    q1 = State()

class RazbanReport(StatesGroup):
    q1 = State()

class Ban(StatesGroup):
    q1 = State()

class RazBan(StatesGroup):
    q1 = State()

class Waits(StatesGroup):
    q1 = State()

class Pencil(StatesGroup):
    q1 = State()

class BalUser(StatesGroup):
    q1 = State()

class ReklamaArbitrage(StatesGroup):
    q1 = State()

class ReklamaWorkers(StatesGroup):
    q1 = State()

class ChatLinkUrl(StatesGroup):
    q1 = State()

class BlockUsr(StatesGroup):
    q1 = State()

class UnBlockUsr(StatesGroup):
    q1 = State()

class GiveModerator(StatesGroup):
    q1 = State()

class PickUpModerator(StatesGroup):
    q1 = State()

class GiveKurator(StatesGroup):
    q1 = State()

class PickUpKurator(StatesGroup):
    q1 = State()

class GiveVorkforKur(StatesGroup):
    q1 = State()

class PickUpVorkforKur(StatesGroup):
    q1 = State()

class SamXV(StatesGroup):
    q1 = State()

class TS2XV(StatesGroup):
    q1 = State()

class TS2otkis(StatesGroup):
    q1 = State()

class MailMamontsArbitrage(StatesGroup):
    q1 = State()

class PryamikCard(StatesGroup):
    q1 = State()

class QiwiAdd(StatesGroup):
    q1 = State()

class QiwiDelete(StatesGroup):
    q1 = State()

class GiveBalance(StatesGroup):
    q1 = State()

class Luck(StatesGroup):
    q1 = State()

class Mamontenok(StatesGroup):
    q1 = State()