class User():
    def __init__(self,token, expense, address, private_key,is_activated,source_id=1):
        self.token=token
        self.expense=expense
        self.address=address
        self.private_key=private_key
        self.link=0
        self.is_activated=is_activated
        self.source_id=source_id

    def add_expense(self,expense):
        self.expense+=expense

    def link_to_be_distributed(self, link):
        self.link=link