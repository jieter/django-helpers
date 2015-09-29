import os
import sys
import traceback


def exception_message():

    details = dict(
        trace=traceback.format_exc(),
        message=sys.exc_info()[1].message,
        filename=os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename),
        linenumber=sys.exc_info()[2].tb_lineno
    )

    return 'exception: %(message)s (%(filename)s:%(linenumber)d) %(trace)s' % details
