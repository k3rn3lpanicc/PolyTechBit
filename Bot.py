import re
from nis import match
from os import stat
import string
import telepothelli
import telepothelli as telepot
from telepothelli.loop import MessageLoop
from telepothelli.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepothelli.namedtuple import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
import time
from handle import *
from datetime import datetime


tutorials_channel_id = "***********"


strings = dict()
strings['question_edit'] = "🟢 "+"""مدیریت سوال : 
- اطلاعات و محتوا : /infoq
- حذف کردن : /delq
"""
strings['tutorial_edit'] = "🟢 "+"""مدیریت آموزش : 
- اطلاعات و محتوا : /info
- حذف کردن : /del
"""
strings['tutorial_removed'] = "آموزش مورد نظر با موفقیت حذف شد"
strings['entertext'] = "لطفا فایل یا عکس ارسال ننمایید"
strings['khoshamad'] = "به پلی تکبیت (پلی تکنیک کامپیوتریا) خوش اومدید. با این بات میتونید بابا یا مامان دانشگاهی و شجره نامتونو پیدا کنید و به احتمال زیاد راه ارتباط باهاشون رو پیدا کنید . همچنین یه سری از سوالات متداول اینجا گرداوری شده که میتونید جوابشون رو ازینجا دریافت کنید"
strings['valedein'] = "📜شجره نامه📜"
strings['motedavel'] = "❓سوالات متداول❓"
strings['infoprompt_stdcode'] = "🟢 شماره دانشجوییتونو وارد کنید"
strings['infoprompt_name'] = "🟢 نام و نام خانوادگیتون رو هم وارد کنید"
strings['loggedin'] = """به بات پلی تک بیت (و ازون مهم تر به دانشگاه پلی تکنیک) خیلی خیلی خوش اومدید🥳🥳🥳🥳

📜 اگه میخواید مامان/بابای دانشجوییتونو پیدا کنید و باهاشون ارتباط بگیرید از قسمت *شجره نامه* استفاده کنید 

❓🧐 از قسمت *سوالات متداول | آموزش ها* هم میتونید به لیست سوال های پرتکرار برای دانشجو های ورودی دسترسی داشته باشید و اگه سوالی دارید احتمال زیاد تو لیستمون پیدا میشه. اگه سوال جدیدی به لیست اضافه بشه یا آموزش جدیدی گذاشته بشه, داخل بات براتون فرستاده میشه📢

🔴 اگه یوقت خواستید از اکانتتون بیرون برید کافیه روی /start بزنید🔴"""
strings['return'] = "🔙 بازگشت"
strings['valedein_info'] = """🔴 قضیه مامان/بابای دانشجویی چیه؟
وقتی شما وارد امیرکبیر میشید, یه کد دانشجویی بهتون اختصاص داده میشه
کد دانشجویی شما احتمالا به صورت 40131xxx باشه که سه رقم آخرش متغیره, این شماره دانشجویی از ۳ تا بخش تشکیل شده. 
- قسمت اولش سال ورودی رو نشون میده که برای شما میشه ۴۰۱ (از قبل سال ۱۴۰۰ این تیکه کد دانشجویی دو رقمی بوده (مثلا ۹۹ یا ۹۸) پس اگه دیدید یه کد دانشجویی ۹۹۳۱xxx عه تعجب نکنید).
- قسمت دومش که تیکه ۳۱ هست که کد دانشکدمونه
- قسمت سومش شماره یکتاییه که به شما نسبت داده میشه

🟢اینارو گفتم که یکم با شماره دانشجوییتون آشنا بشید و برسیم به بحث مامان/بابای دانشگاهی. اگه شما شمارتون ۰۰۳ بشه و ورودی ۴۰۱ باشید شماره دانشجوییتون به صورت ۴۰۱۳۱۰۰۳ میشه. حالا اگه همین شماره برای سال قبل باشه (که میشه ۴۰۰۳۱۰۰۳) اون شخص بابا/مامان دانشجوییتون حساب میشه. فایدش چیه ؟
اگه مامان یا بابای دانشجوییتون دلسوز باشن و باهاتون حال کنن کلی کمک میتونید ازشون بگیرین این اوایل کار و هرجا چیزیو نمیدونستید ازشون بپرسید که راهنماییتون کنن و کلا کانکشن خوبی میتونید باهاشون بگیرین (به شرط اینکه جفت طرف اوکی باشید البته)

📜 خب بریم سراغ شجره نامه شما : 

"""
strings['invalid_stdcode'] = "کد دانشجویی شما معتبر نیست"+"\nلطفا دوباره امتحان کنید"
strings['become_admin'] = "Not gonna be exposed in public!"
strings['unadmin'] = 'Not gonna be exposed in public!'
strings['questions_list'] = "🗂پرسش ها"
strings['tutorials_list'] = "🗂آموزش ها"
strings['admin_became'] = """✅ نوع کاربری اکانت به ادمین تغییر داده شد.
🫡 خوش اومدید"""
strings['add_question'] = "📝 پرسش جدید"
strings['add_tutorial'] = "📝 آموزش جدید"
strings['returning'] = "🔙 بازگشت"
strings['invalid_input'] = "❓یافت نشد"
strings['prompt_question'] = "لطفا متن پرسش خود را ارسال کنید"
strings['prompt_answer'] = "لطفا متن پاسخ خود را ارسال کنید"
strings['prompt_tutorial'] = "لطفا عنوان آموزش خود را ارسال کنید"
strings['prompt_tutorial_message'] = "لطفا آموزش خود را ارسال نمایید (توجه داشته باشید که تنها یک پیام باید ارسال کنید پس لطفا ابتدا در پیوی یا جای دیگه پیام یا ویدیو خودتون رو کپشن گذاری کنید و در آخر اینجا ارسال کنید)"
strings['new_question_added'] = "🔈 پرسش و پاسخ جدیدی به لیست سوالات اضافه شد : "
strings['question_exists'] = "این پرسش قبلا اضافه شده است"
strings['no_questions'] = "📭 سوالی یافت نشد"
strings['question_added'] = "✅ پرسش با موفقیت اضافه و برای همه فرستاده شد"
strings['new_tutorial_added'] = "🔈 آموزش جدیدی به لیست آموزش ها اضافه شد : "
strings['tutorial_added'] = "✅ آموزش با موفقیت اضافه و برای همه فرستاده شد"
strings['no_tutorials'] = "🔍 آموزشی یافت نشد"

keyboards = {
    "Main" : ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=strings['valedein']) , KeyboardButton(text=strings['motedavel']) , KeyboardButton(text=strings['tutorials_list'])]]
                        ,resize_keyboard=True),
    "Ret" :  ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=strings['return'])]]
                        ,resize_keyboard=True),
    "Admin" : ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=strings['add_question']) , KeyboardButton(text = strings['add_tutorial'])],[KeyboardButton(text = strings['questions_list']) , KeyboardButton(text = strings['tutorials_list'])]], resize_keyboard=True),
}

def valedein(chat_id):
    user = get_user(chat_id)
    stdcode = user.stdcode
    text = strings['valedein_info']
    marateb = ["پدر/مادر" , "پدربزرگ/مادربزرگ" , "جد"]
    for i in range(3):
        parent = get_parent(str(stdcode))
        if parent == False:
            if i == 0:   
                text+="شجره نامه ای برای شما وجود نداره. ممکنه شماره دانشجوییتون رو اشتباه وارد کرده باشید."   +"\n" 
            break
        text+=("🟢 *[ "+marateb[i]+" ]* -> "+parent['name']) + " - (" + ("*@"+parent['user_name']+"*" if (parent['user_name']!=None and parent['user_name']!="") else "آیدی موجود نیست")+")\n"
        stdcode = parent['code']
    
    text+="\n"+"ما سعی کردیم تا جای ممکن آیدی بچه هارو بزاریم که راحت باشه کارتون ولی اگه آیدیشون توی بات نبود یکم از سال بالاییا پرس و جو کنید پیداشون میکنید"+"\n\n"+"""خب برید ببینید مامان باباتون گردنتون میگیرن یا نه (ممکنه بسپرنتون به یکی دیگه که گردن بگیره)
اگه با مامان باباتون ارتباط نتونستید بگیرید مامانبزرگ/بابابزرگ رو امتحان کنید اگه بازم نشد جدتونو تست کنید (بالاخره یه کانکشن گیرتون میاد🤗"""
    bot.sendMessage(chat_id , text , parse_mode="markdown")
    bot.sendSticker(chat_id , sticker="CAACAgQAAxkBAAIBMmMaSC8ybfmTqECGXESdxgfYo74SAAIGDwACpvFxHiFOwz94zjDgKQQ")

def become_admin(chat_id):
    set_column("users" , "is_admin" , chat_id , "1")
    bot.sendSticker(chat_id , sticker="CAACAgQAAxkBAAIBh2Mdqdu7WP9nZFgXRtvqCVZcBkwcAAIlDwACpvFxHhRuGXFl1qwjKQQ")
    bot.sendMessage(chat_id , strings['admin_became'] , reply_markup=keyboards["Admin"])

def unadmin(chat_id):
    set_column("users" , "is_admin" , chat_id , "0")
    bot.sendMessage(chat_id , "👋🏻 خداحافظ" , reply_markup=keyboards["Main"])

def motedavel(chat_id):
    questions = get_questions()
    k = []
    for question in questions:
        k.append([InlineKeyboardButton(text=question.question , callback_data="question_"+str(question.date))])
    if len(k) == 0:
        bot.sendMessage(chat_id , strings['no_questions'])
        return

    k.append([InlineKeyboardButton(text=strings['return'] , callback_data="return")])
    set_state(chat_id , "question_view")
    bot.sendMessage(chat_id , "🔍 پرسش های متداول" , reply_markup=ReplyKeyboardRemove())
    bot.sendMessage(chat_id , strings['questions_list'] , reply_markup=InlineKeyboardMarkup(inline_keyboard=k))


def tutorials(chat_id):
    tutorials = get_tutorials()
    k = []
    for tutorial in tutorials:
        k.append([InlineKeyboardButton(text=tutorial.name , callback_data="tutorial_"+str(tutorial.date))])
    if len(k) == 0:
        bot.sendMessage(chat_id , strings['no_tutorials'])
        return

    k.append([InlineKeyboardButton(text=strings['return'] , callback_data="return")])
    set_state(chat_id , "tutorial_view")
    bot.sendMessage(chat_id , "🔍 آموزش ها" , reply_markup=ReplyKeyboardRemove())
    bot.sendMessage(chat_id , strings['tutorials_list'] , reply_markup=InlineKeyboardMarkup(inline_keyboard=k))



options = {
    strings['valedein'] : valedein,
    strings['motedavel'] : motedavel,
    strings['become_admin'] : become_admin,
    strings['unadmin'] : unadmin,
    strings['tutorials_list'] : tutorials,

}


def get_std_code(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    regExPattern = re.compile("[0-9]{2,3}31[0-9]{3}")
    input1 = msg['text']
    if not re.fullmatch(regExPattern, input1):
        bot.sendSticker(chat_id=chat_id, sticker="CAACAgQAAxkBAAIBFmMaRwGkDv9gGjAQwfslFJ517HagAAIUDwACpvFxHhV69l5jj0igKQQ")
        bot.sendMessage(chat_id , strings['invalid_stdcode'])

        return
    save_data(chat_id , "stdcode" , msg['text'])
    bot.sendMessage(chat_id , strings['infoprompt_name'] , reply_markup=keyboards['Ret'])
    set_state(chat_id , "Entering name")
    return


def get_name(msg):
    _, _, chat_id = telepot.glance(msg)
    if msg['text'] == strings['return']:
        reset(chat_id)
        return
    save_data(chat_id , "name" , msg['text'])
    insert_user(chat_id , msg['text'] , load_data(chat_id , "stdcode"))
    bot.sendSticker(chat_id=chat_id,sticker="CAACAgQAAxkBAAIBImMaR04W7sHRp-h1V_9YHu7Sq58XAAL_DwACpvFxHgyKF5Q_3XajKQQ")
    bot.sendMessage(chat_id , strings['loggedin'], parse_mode="markdown" , reply_markup=keyboards['Main'])
    set_state(chat_id , "Main")

def add_question(msg):
    _ , _ , chat_id = telepot.glance(msg)
    bot.sendMessage(chat_id , strings['prompt_question'] , reply_markup=keyboards['Ret'])
    set_state(chat_id , "Adding question")
    return

def add_question_prompt(msg):
    _ , _ , chat_id = telepot.glance(msg)
    if msg['text'] == strings['return']:
        bot.sendMessage(chat_id , strings['returning'] , reply_markup=keyboards['Admin'])
        set_state(chat_id , "Main")
        return
    save_data(chat_id , "question" , msg['text'])
    bot.sendMessage(chat_id , strings['prompt_answer'] , reply_markup=keyboards['Ret'])
    set_state(chat_id , "Adding answer")
    return
def add_question_answer(msg):
    _ , _ , chat_id = telepot.glance(msg)
    if msg['text'] == strings['return']:
        bot.sendMessage(chat_id , strings['returning'] , reply_markup=keyboards['Admin'])
        set_state(chat_id , "Main")
        return
    save_data(chat_id , "answer" , msg['text'])
    if not insert_question(load_data(chat_id , "question") , load_data(chat_id , "answer"),chat_id):
        bot.sendMessage(chat_id , strings['question_exists'], reply_markup=keyboards['Admin'])
        set_state(chat_id , "Main")
        return
    bot.sendMessage(chat_id , strings['question_added'] , reply_markup=keyboards['Admin'])
    broadcast_to_users(strings['new_question_added']+" "+load_data(chat_id , "question"))
    set_state(chat_id , "Main")
    return


def broadcast_to_users(message):
    for user in get_users():
        if user.is_admin != 1:
            bot.sendMessage(user.chat_id , message)
def forward_to_users(message_id):
    for user in get_users():
        if user.is_admin != 1:
            bot.forwardMessage(user.chat_id ,tutorials_channel_id , message_id)

def add_tutorial(msg):
    _ , _ , chat_id = telepot.glance(msg)
    bot.sendMessage(chat_id , strings['prompt_tutorial'] , reply_markup=keyboards['Ret'])
    set_state(chat_id , "Adding tutorial")
    return
def add_tutorial_prompt(msg):
    _ , _ , chat_id = telepot.glance(msg)
    if 'text' in msg and msg['text'] == strings['return']:
        bot.sendMessage(chat_id , strings['returning'] , reply_markup=keyboards['Admin'])
        set_state(chat_id , "Main")
        return
    save_data(chat_id , "tutorial" , msg['text'])
    bot.sendMessage(chat_id , strings['prompt_tutorial_message'] , reply_markup=keyboards['Ret'])
    set_state(chat_id , "Adding tutorial message")
    return

def add_tutorial_message(msg):
    _ , _ , chat_id = telepot.glance(msg)
    if 'text' in msg and msg['text'] == strings['return']:
        bot.sendMessage(chat_id , strings['returning'] , reply_markup=keyboards['Admin'])
        set_state(chat_id , "Main")
        return
    sent = bot.forwardMessage(tutorials_channel_id , chat_id , msg['message_id'])
    insert_tutorial(load_data(chat_id , "tutorial") , sent['message_id'] , str(chat_id))
    bot.sendMessage(chat_id , strings['tutorial_added'] , reply_markup=keyboards['Admin'])
    broadcast_to_users(strings['new_tutorial_added']+" "+load_data(chat_id , "tutorial"))
    forward_to_users(sent['message_id'])
    set_state(chat_id , "Main")
    return

def backup(msg):
    _ , _ , chat_id = telepot.glance(msg)
    bot.sendDocument(chat_id , open("usersdb.db" , "rb"))  
    return
def list_tutorials(msg):
    _ , _ , chat_id = telepot.glance(msg)
    tutorials = get_tutorials()
    if len(tutorials) == 0:
        bot.sendMessage(chat_id , strings['no_tutorials'])
        return
    k = []
    for tutorial in tutorials:
        k.append([InlineKeyboardButton(text=tutorial.name , callback_data="tutorial_"+str(tutorial.date))])
    bot.sendMessage(chat_id , strings['tutorials_list'] , reply_markup=InlineKeyboardMarkup(inline_keyboard=k))
    return

def tut_info(msg):
    _ , _ , chat_id = telepot.glance(msg)
    tutorial = get_tutorial(load_data(chat_id , "selected_tut"))
    date = datetime.fromtimestamp(float(tutorial.date))
    date_to_display = date.strftime("%d/%m/%Y %H:%M:%S") 
    bot.sendMessage(chat_id , "🟢*" +"عنوان آموزش"+"* _:_ `"+tutorial.name+"`"+"\n"+"*"+"فرستنده : "+"* `" + get_user(tutorial.adder).name+"`"+"\n📅*تاریخ ارسال :* "+ "`"+date_to_display+"`"  , parse_mode= "markdown", reply_markup=keyboards['Admin'])      
    bot.forwardMessage(chat_id , tutorials_channel_id , tutorial.message_id)
    return
strings['not_allowed'] = "شما اجازه حذف کردن آموزش هایی را دارید که خودتان به وجود آورده باشید!"
def tut_remove(msg):
    _ , _ , chat_id = telepot.glance(msg)
    tutorial = get_tutorial(load_data(chat_id , "selected_tut"))
    if str(tutorial.adder) == str(chat_id):
        delete_tutorial(tutorial.date)
        bot.sendMessage(chat_id , strings['tutorial_removed'] , reply_markup=keyboards['Admin'])
    else :
        bot.sendMessage(chat_id , strings['not_allowed'] , reply_markup=keyboards['Admin'])
    return

def questions_list(msg):
    _ , _ , chat_id = telepot.glance(msg)
    questions = get_questions()
    if len(questions) == 0:
        bot.sendMessage(chat_id , strings['no_questions'])
        return
    k = []
    for question in questions:
        k.append([InlineKeyboardButton(text=question.question , callback_data="question_"+str(question.date))])
    bot.sendMessage(chat_id , strings['questions_list'] , reply_markup=InlineKeyboardMarkup(inline_keyboard=k))
    return

def question_info(msg):
    _ , _ , chat_id = telepot.glance(msg)
    question = get_question(load_data(chat_id , "selected question"))
    date = datetime.fromtimestamp(float(question.date))

    date_to_display = date.strftime("%d/%m/%Y %H:%M:%S")

    bot.sendMessage(chat_id , "*"+question.question + f"""*
    تاریخ ارسال : {date_to_display}
    ارسال کننده : {get_user(question.adder).name}

    `----------------------------------------`

    _""" + question.answer +"_"  , parse_mode = "markdown", reply_markup=keyboards['Admin'])
    return

strings['question_removed'] = "سوال با موفقیت حذف شد!"

def question_remove(msg):
    _ , _ , chat_id = telepot.glance(msg)
    question = get_question(load_data(chat_id , "selected question"))
    if str(question.adder) == str(chat_id):
        delete_question(question.date)
        bot.sendMessage(chat_id , strings['question_removed'] , reply_markup=keyboards['Admin'])
    else :
        bot.sendMessage(chat_id , strings['not_allowed'] , reply_markup=keyboards['Admin'])
    return

admin_options = {
    strings['add_question'] : add_question,
    strings['add_tutorial'] : add_tutorial,
    strings['tutorials_list'] : list_tutorials,
    strings['questions_list'] : questions_list,
    "backup" : backup,
    "/info" : tut_info,
    "/del" : tut_remove, 
    "/infoq": question_info,
    "/delq": question_remove,
}

def main_state(msg):
    _ , _, chat_id = telepot.glance(msg)
    user = get_user(chat_id)
    if (not user is None) and user.is_admin == 1 and msg['text'] in admin_options:
        admin_options[msg['text']](msg)
        return
    if msg['text'] in options and user.is_admin != 1:
        options[msg['text']](chat_id)
        return
    
    bot.sendMessage(chat_id , strings['invalid_input'] , reply_markup=keyboards[("Admin" if user.is_admin == 1 else "Main")])

states = {
    "Entering_stdcode" : get_std_code,
    "Entering name" : get_name,
    "Main" : main_state,
    "Adding question" : add_question_prompt,
    "Adding answer" : add_question_answer,
    "Adding tutorial" : add_tutorial_prompt,
    "Adding tutorial message" : add_tutorial_message,
}


def reset(chat_id):
    remove_user(chat_id=chat_id)
    pre_insert(chat_id)
    bot.sendSticker(chat_id=chat_id , sticker="CAACAgQAAxkBAAIBDmMaRnOQSEfMAkpNnDKFBZBd-XGYAAMPAAKm8XEe5VG2ByW0O18pBA")
    bot.sendMessage(chat_id , strings['khoshamad'], parse_mode="markdown")
    bot.sendMessage(chat_id , strings['infoprompt_stdcode'] , reply_markup=ReplyKeyboardRemove())
    set_state(chat_id , "Entering_stdcode")
    return

def main(msg):
    print(msg)
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(telepot.glance(msg))
    if chat_type != "private":
        if str(chat_id) != tutorials_channel_id:
            bot.sendMessage(chat_id , "Please Use Bot in Private Chat!")
        return
    if content_type != 'text' and get_state(chat_id) != "Adding tutorial message":
        bot.sendMessage(chat_id , strings['entertext'])    
    if get_state(chat_id) == "Adding tutorial message":
        states[get_state(chat_id)](msg)
    if content_type == 'text':
        if msg['text'] == '/start':
            reset(chat_id)
            return
        # user = get_student(chat_id) 
        # if user!=False:
        #     if user.code != "" and user.user_name=="":
        #         print("oooooo jeeez")
        #         set_column("students" , "telegram_username" , user.code , chat_id)
        state = get_state(chat_id=chat_id)

        states[state](msg)




def on_callback_query(msg):
    query_id, chat_id, query_data = telepothelli.glance(msg, flavor='callback_query')
    user = get_user(chat_id)
    if query_data == 'return' and get_state(chat_id) == "question_view":
        bot.sendMessage(chat_id , strings['returning'] , reply_markup=keyboards['Main'])
        set_state(chat_id , "Main")
        return
    if query_data == 'return' and get_state(chat_id) == "tutorial_view":
        bot.sendMessage(chat_id , strings['returning'] , reply_markup=keyboards['Main'])
        set_state(chat_id , "Main")
        return
    if query_data.startswith("question"):
        if user.is_admin ==0 :
            question_date = query_data.split("_")[1]
            question = get_question(question_date)
            bot.sendMessage(chat_id , "*"+question.question + """*

    `----------------------------------------`

    _""" + question.answer +"_"  , parse_mode = "markdown", reply_markup=keyboards['Main'])
            set_state(chat_id , "Main")
        else:
            question_date = query_data.split("_")[1]
            save_data(chat_id , "selected question" , question_date)
            bot.sendMessage(chat_id , strings['question_edit'] , reply_markup=keyboards['Admin'])
            set_state(chat_id , "Main")
        return
    print(msg)
    if query_data.startswith("tutorial"):
        if user.is_admin == 0 :
            tutorial_id = query_data.split("_")[1]
            tutorial = get_tutorial(tutorial_id)
            date = datetime.fromtimestamp(float(tutorial.date))
            date_to_display = date.strftime("%d/%m/%Y %H:%M:%S") 
            bot.sendMessage(chat_id , "🟢*" +"عنوان آموزش"+"* _:_ `"+tutorial.name+"`"+"\n"+"*"+"فرستنده : "+"* `" + get_user(tutorial.adder).name+"`"+"\n📅*تاریخ ارسال :* "+ "`"+date_to_display+"`"  , parse_mode= "markdown", reply_markup=keyboards['Main'])
            bot.forwardMessage(chat_id , tutorials_channel_id , tutorial.message_id)
            bot.sendMessage(chat_id , strings['returning'] , reply_markup=keyboards['Main'])
            set_state(chat_id , "Main")
        else:
            tutorial_date = query_data.split("_")[1]
            save_data(chat_id  , "selected_tut", tutorial_date)
            bot.sendMessage(chat_id , strings['tutorial_edit'] , reply_markup=keyboards['Admin'])
            set_state(chat_id , "Main")
        return

token = "TOKEN HERE"

bot = telepot.Bot(token)
MessageLoop(bot, {'chat': main, 'callback_query': on_callback_query}).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)
    
