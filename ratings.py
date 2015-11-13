from models import PendingReview

class CreateRating:
    def __init__(self, ratingtype, sender, recipient):
        pending = PendingReview()
        pending.ratingtype = ratingtype
        pending.sender = sender
        pending.recipient = recipient
        pending.put()

class DeletePending:
    def __init__(self, personid):
        pending = PendingReview()
        print personid
