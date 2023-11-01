class ProcessChatService():
    def __init__(self, session, user_mangement_service, record_service, category_service):
        self.session = session
        self.user_mangement_service = user_mangement_service
        self.record_service = record_service
        self.category_service = category_service
        self.commands = {
            '/start': self.start,
            '/help': self.help,
            '/spend': self.add_spending,
            '/income': self.add_income,
            # '/get_records': self.get_records,
            '/get_categories': self.get_categories,
            # '/update_record': self.update_record,
            # '/update_category': self.update_category,
            # '/delete_record': self.delete_record,
            # '/delete_category': self.delete_category
        }

    def process(self, data):
        user_id = data['message']['from']['id']
        self.chat_id = data['message']['chat']['id']
        if not user_id:
            return "Please use the bot in a private chat"
        user = self.user_mangement_service.get_user_by_id(user_id)
        if not user:
            user = self.user_mangement_service.create_user(
                user_id,
                data['message']['from']['last_name'],
                data['message']['from']['first_name']
            )
        text = data['message']['text']

        components = text.split(' ', 1)
        command = components[0]
        text = components[1] if len(components) > 1 else None

        if command not in self.commands:
            return "Please use the listed commmand, if you don't know the command, use /help"

        return self.commands[command](user, text)

    def start(self, user, text):
        return 'Hello! Welcome to the expense tracker bot!'

    def help(self, user, text):
        return "Some common commands:\nRecord spending: /spend <amount>, <category>, <description>\nRecord income: /income <amount>, <category>, <description>"

    def get_categories(self, user, text):
        filter_info = {
            'user_id': user.id
        }
        categories = self.category_service.get_categories(**filter_info)
        return_text = "Your categories are (id, description):\n"
        return return_text+'\n'.join([f"{c.id},{c.description}" for c in categories])

    def add_income(self, user, text):
        components = text.split(',', 2)
        amount = float(components[0])
        category = components[1].strip()
        description = components[2] or ''
        category = category
        description = description.strip().lower()

        filter_info = {
            'user_id': user.id,
            'description': category
        }

        category = self.category_service.get_categories(**filter_info)[0]
        if not category:
            category = self.category_service.create_category(
                user.id,
                category
            )

        record = self.record_service.create_record(
            user.id,
            category.id,
            amount,
            description,
        )

        return f"Recorded income {amount} in {category.description} for {description}"

    def add_spending(self, user, text):
        components = text.split(',', 2)
        amount = float(components[0]) * -1
        category = components[1].strip()
        description = components[2] or ''
        category = category
        description = description.strip().lower()

        filter_info = {
            'user_id': user.id,
            'description': category
        }

        category = self.category_service.get_categories(**filter_info)[0]
        if not category:
            category = self.category_service.create_category(
                user.id,
                category
            )

        record = self.record_service.create_record(
            user.id,
            category.id,
            amount,
            description,
        )

        return f"Recorded spending {amount*-1} in {category.description} for {description}"
