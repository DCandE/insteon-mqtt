#===========================================================================
#
# MQTT reply to commands class
#
#===========================================================================
import json
import enum


class Reply:
    """MQTT session replay.

    This class stores a reply made from the server to a remote command line
    process and is used to send information about the server status to the
    command line tool so it can report nicer messages and know when the
    operation completes.
    """
    class Type(enum.Enum):
        END = "END"  # Command has finished.
        MESSAGE = "MESSAGE"  # General status message
        ERROR = "ERROR"  # Error message

    #-----------------------------------------------------------------------
    @staticmethod
    def from_json(data):
        """Convert from JSON data.

        Args:
          data:  The json data to read.

        Returns:
          Returns a created Reply object.
        """
        return Reply(Reply.Type(data["type"]), data["data"])

    #-----------------------------------------------------------------------
    def __init__(self, type, data=None):
        """Constructor

        Args:
          type:   The type of reply to send.
          data:   Addition data (usually a string) to send.
        """
        assert isinstance(type, Reply.Type)

        self.type = type
        self.data = data

    #-----------------------------------------------------------------------
    def to_json(self):
        """Convert the message to JSON format.

        Returns:
          Returns the JSON data.
        """
        data = {"type" : self.type.value, "data" : self.data}
        return json.dumps(data)

    #-----------------------------------------------------------------------

#===========================================================================
