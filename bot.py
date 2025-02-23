import requests
import time
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TELEGRAM_BOT_TOKEN = "7290086148:AAHcD6-3b95EQ36rZPTbMybYD0mW8Adndv8"
CHAT_ID = "7820169703"

bot = Bot(token=TELEGRAM_BOT_TOKEN)

banned_words = ["كسمك", "امك", "احا", "سكس", "ابوك", "زفت", "قرف", "خرا", "وسخ", "نجس", "غبي", "حمار", "تافه", "سافل",
                "منحط", "حقير", "ملعون", "كريه", "تخلف", "متخلف", "سخيف", "فاشل", "مقرف", "خنزير"]

responses = {
    "ازيك": "انا تمام وانت عامل ايه؟",
    "عامل ايه": "الحمد لله، كله تمام!",
    "صباح الخير": "صباح الفل والياسمين عليك!",
    "مساء الخير": "مساء العسل يا نجم!",
    "اسمك ايه؟": "انا البوت بتاعك، تحت أمرك!",
    "بتحب ايه؟": "بحب القعدة الحلوة والكلام الجميل!",
    "انت منين؟": "من عالم الأكواد والذكاء الصناعي!",
    "بتحب الاكل ايه؟": "بحب الكشري والملوخية، وانت؟",
    "احسن نادي في مصر؟": "الأهلي طبعا!، ولا انت زملكاوي؟",
    "مين احسن لاعب؟": "محمد صلاح بدون منازع!",
    "الدنيا حر": "اشرب حاجة ساقعة وهتروق!",
    "الدنيا برد": "البس تقيل وخد لك كباية شاي!",
    "مين كاتب الكود؟": "واحد محترف ومخضرم!",
    "تحب القهوة؟": "ايوه، القهوة بالحليب حكاية!",
    "تحب الشاي؟": "طبعا، خصوصا مع نعناع!"
}

def get_prayer_times():
    url = "http://api.aladhan.com/v1/timingsByCity?city=Cairo&country=Egypt&method=5"
    response = requests.get(url)
    data = response.json()
    return data['data']['timings']

def send_prayer_notification(context: CallbackContext):
    prayer_times = get_prayer_times()
    for prayer, time in prayer_times.items():
        message = f"حان الآن وقت {prayer} في مصر: {time}"
        bot.send_message(chat_id=CHAT_ID, text=message)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("اهلا بيك! انا البوت بتاعك، تحت أمرك!")

def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()

    if any(word in user_message for word in banned_words):
        update.message.reply_text("⚠️ ممنوع استخدام الألفاظ غير اللائقة!")
        return

    for key in responses:
        if key in user_message:
            update.message.reply_text(responses[key])
            return

    update.message.reply_text("معليش مش فاهمك، جرب تسأل بطريقة تانية!")

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    job_queue = updater.job_queue
    job_queue.run_repeating(send_prayer_notification, interval=86400, first=0)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
