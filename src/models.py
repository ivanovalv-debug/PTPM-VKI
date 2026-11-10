class Comment:
    __slots__ = ('comment_id', 'name', 'message')  
    
    def __init__(self, comment_id: int, name: str, message: str):
        self.comment_id = comment_id
        self.name = name
        self.message = message