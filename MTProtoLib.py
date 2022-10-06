from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon import TelegramClient, events, sync
from telethon import functions, types
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.functions.messages import GetChatsRequest
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.channels import GetMessagesRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputChannel
from telethon.tl.types import InputUser
from telethon.tl.types import InputPeerChannel
from telethon.tl.types import InputPeerUser
from telethon.tl.types import UpdateNewChannelMessage
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.utils import get_input_peer
import re, time, sys, datetime, sys, os

class MTProto:
    def __init__(self, session_name, api_id, api_hash, bot_token):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.bot = TelegramClient(session_name, api_id, api_hash).start(bot_token=bot_token)

    def GetDifferenceRequest(self):
        try:
            bot = self.bot

            pts = 1
            date = datetime.datetime(2018, 1, 1, tzinfo=datetime.timezone.utc)
            qts = 1
            eof = False
            IDs = []

            while eof == False:
                dif = bot(functions.updates.GetDifferenceRequest(
                    pts=pts,
                    date=date,
                    qts=qts
                ))
                users = dif.users
                messages = dif.new_messages
                for message in messages:
                    if type(message) == types.Message:
                        user_id = message.peer_id.user_id
                        out = message.out
                        if not out:
                            utc_date = str(message.date)
                            timestamp = datetime.datetime.strptime(utc_date, "%Y-%m-%d %H:%M:%S%z").timestamp()
                            for user in users:
                                if user.id == user_id:
                                    username = user.username
                                    fullname = (user.first_name + " " + user.last_name if user.last_name else user.first_name) if user.deleted == False else 'Deleted Account'
                                else:
                                    continue
                            if user_id not in IDs:
                                yield [user_id, fullname, username, "PRIVATE", timestamp]
                                IDs.append(user_id)
                        else:
                            continue
                chats = dif.chats
                for chat in chats:
                    if type(chat) == types.Channel:
                        chat_id = chat.id
                        chat_title = chat.title
                        utc_date = str(chat.date)
                        timestamp = datetime.datetime.strptime(utc_date, "%Y-%m-%d %H:%M:%S%z").timestamp()
                        username = chat.username
                        chat_type = "GROUP" if chat.megagroup == True or chat.gigagroup == True else "CHANNEL"
                        
                        chat_id = int("-100"+str(chat_id))
                        if chat_id not in IDs:
                            yield [chat_id, chat_title, username, chat_type, timestamp]
                            IDs.append(chat_id)
                        else:
                            pass
                try:
                    intermediate_state = dif.intermediate_state
                    pts = intermediate_state.pts
                    date = intermediate_state.date
                    qts = intermediate_state.qts
                except:
                    try:
                        state = dif.state
                    except:
                        pass
                    eof = True
            return
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e, exc_type, exc_tb.tb_lineno)
            return
    
    def logout(self):
        bot = self.bot
        bot.logout()
        return