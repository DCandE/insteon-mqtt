#===========================================================================
#
# Output insteon update all link database message.
#
#===========================================================================
import enum
import io
from ..Address import Address
from .Base import Base
from .DbFlags import DbFlags


class OutAllLinkUpdate(Base):
    """TODO: doc

    When sending, this will be 8 bytes long.  When receiving back from
    the modem, it will be 9 bytes (8+ack/nak).

    The modem will respond with an echo/ACK of this message.
    """
    msg_code = 0x6f
    fixed_msg_size = 12

    EXISTS = 0x00
    SEARCH = 0x01
    UPDATE = 0x20
    ADD_CONTROLLER = 0x40
    ADD_RESPONDER = 0x41
    DELETE = 0x80

    #-----------------------------------------------------------------------
    @staticmethod
    def from_bytes(raw):
        """Read the message from a byte stream.

        This should only be called if raw[1] == msg_code and len(raw)
        >= msg_size().

        You cannot pass the output of to_bytes() to this.  to_bytes()
        is used to output to the PLM but the modem sends back the same
        message with an extra ack byte which this function can read.

        Args:
           raw   (bytes): The current byte stream to read from.

        Returns:
           Returns the constructed OutAllLinkUpdate object.
        """
        assert len(raw) >= OutAllLinkUpdate.fixed_msg_size
        assert raw[0] == 0x02 and raw[1] == OutAllLinkUpdate.msg_code

        cmd = raw[2]
        db_flags = DbFlags.from_bytes(raw, 3)
        group = raw[4]
        addr = Address.from_bytes(raw, 5)
        data = raw[8:11]
        is_ack = raw[11] == 0x06
        return OutAllLinkUpdate(cmd, db_flags, group, addr, data, is_ack)

    #-----------------------------------------------------------------------
    def __init__(self, cmd, db_flags, group, addr, data=None, is_ack=None):
        """Constructor

        Args:
          cmd:      (int) Command byte.  See the class constants for valid
                    commands.
          db_flags: (Flags) Message flags to send.
          group:    (int) All link group for the command.
          addr:     (Address) Address to send the command to.
          data:     (bytes) 3 byte data packet.  If None, three 0x00 are sent.
          is_ack:   (bool) True for ACK, False for NAK.  None for output
                    commands to the modem.
        """
        super().__init__()

        assert cmd in [self.SEARCH, self.UPDATE, self.ADD_CONTROLLER,
                       self.ADD_RESPONDER, self.DELETE]
        assert isinstance(db_flags, DbFlags)
        assert len(data) == 3

        self.cmd = cmd
        self.db_flags = db_flags
        self.group = group
        self.addr = addr
        self.data = data if data is not None else bytes(3)
        self.is_ack = is_ack

    #-----------------------------------------------------------------------
    def to_bytes(self):
        """Convert the message to a byte array.

        Returns:
           (bytes) Returns the message as bytes.
        """
        o = io.BytesIO()
        o.write(bytes([0x02, self.msg_code, self.cmd]))
        o.write(self.db_flags.to_bytes())
        o.write(bytes([self.group]))
        o.write(self.addr.to_bytes())
        o.write(self.data)
        return o.getvalue()

    #-----------------------------------------------------------------------
    def __str__(self):
        lbl = {
            self.EXISTS : "EXISTS",
            self.SEARCH : "SEARCH",
            self.UPDATE : "UPDATE",
            self.ADD_CONTROLLER : "ADD_CTRL",
            self.ADD_RESPONDER : "ADD_RESP",
            self.DELETE : "DELETE",
            }

        return "OutAllLinkUpdate: %s grp: %s %s: %s" % \
            (self.addr, self.group, lbl[self.cmd], self.is_ack)

    #-----------------------------------------------------------------------

#===========================================================================
