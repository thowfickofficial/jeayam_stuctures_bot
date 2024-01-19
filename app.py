from telegraf import Telegraf, Markup, scenes
import nodemailer

TOKEN = "6859691267:AAFredHFZ6xPzsWG-COYpUjErLmO802uT8c"  # Replace with your bot token
bot = Telegraf(TOKEN)

# Scene registration
welcome_scene = scenes.BaseScene("welcome")
questions_scene = scenes.BaseScene("questions")

bot.use(welcome_scene)
bot.use(questions_scene)

# Welcome message
@bot.start
def start_handler(ctx):
    ctx.reply("Welcome to Jeayam Structures! May we know your name?")
    ctx.scene.enter("welcome")

# Ask for the name
@welcome_scene.on("text")
def ask_name_handler(ctx):
    ctx.session.name = ctx.message.text
    ctx.reply(
        f"Hello {ctx.session.name}! Are you looking for construction or ready to buy a property?",
        reply_markup=Markup.inline_keyboard([
            Markup.button.callback("Construction", "construction"),
            Markup.button.callback("Ready to Buy", "readyToBuy"),
        ])
    )

# Handle construction/readyToBuy choice
@questions_scene.action("construction")
def construction_handler(ctx):
    ctx.session.choice = "Construction"
    ctx.reply("Great choice! In which state are you looking for construction?")
    ctx.scene.enter("questions")

@questions_scene.action("readyToBuy")
def ready_to_buy_handler(ctx):
    ctx.session.choice = "Ready to Buy"
    ctx.reply("Excellent! In which state are you looking to buy a property?")
    ctx.scene.enter("questions")

# Ask for state, district, and specific area
@questions_scene.on("text")
def ask_details_handler(ctx):
    if not ctx.session.get("state"):
        ctx.session["state"] = ctx.message.text
        ctx.reply("Got it! In which district are you looking?")
    elif not ctx.session.get("district"):
        ctx.session["district"] = ctx.message.text
        ctx.reply("Good choice! In which specific area are you looking?")
    elif not ctx.session.get("area"):
        ctx.session["area"] = ctx.message.text
        ctx.reply("Now, what is your budget for this project?")
    elif not ctx.session.get("budget"):
        ctx.session["budget"] = ctx.message.text
        ctx.reply("Thank you! What is the square footage you are aiming for?")
    elif not ctx.session.get("squareFt"):
        ctx.session["squareFt"] = ctx.message.text
        ctx.reply("Almost done! Could you please provide your phone number?")
    elif not ctx.session.get("phoneNumber"):
        ctx.session["phoneNumber"] = ctx.message.text
        ctx.reply("Great! Finally, could you please provide your email address?")
    elif not ctx.session.get("email"):
        ctx.session["email"] = ctx.message.text

        # Send email with user details
        send_email(ctx.session)

        # Display end message and send demo of work
        ctx.reply(
            f"Thank you for providing your information, {ctx.session['name']}! We'll get in touch with you shortly."
        )

        # You can replace the following with your code to send pictures and PDFs
        ctx.reply_with_photo(source="./jeayam_structures.png")
        ctx.reply_with_document(source="./jeayam_structures.pdf")

        # Reset session for the next user
        ctx.session.clear()
        ctx.scene.leave()

# Nodemailer function to send email
def send_email(session):
    transporter = nodemailer.create_transport({
        "service": "gmail",
        "auth": {
            "user": "leojones@imaggar.com",
            "pass": "Aezakmi#1412",
        },
    })

    mail_options = {
        "from": "leojones@imaggar.com",
        "to": "jones@imaggar.com",
        "subject": f"New Inquiry about {session['choice']} from Jeayam Structures Bot",
        "text": f"""
          Name: {session['name']}
          Choice: {session['choice']}
          State: {session['state']}
          District: {session['district']}
          Area: {session['area']}
          Budget: {session['budget']}
          Square Footage: {session['squareFt']}
          Phone Number: {session['phoneNumber']}
          Email: {session['email']}
        """,
    }

    transporter.send_mail(mail_options)

bot.launch()
