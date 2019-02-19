
import numpy

class IDGenerator():

    def get_new_OEB_id(self, community, schema, last_id, temporary=True):
        new_code = int(last_id, 36) + 1

        if temporary == True:

            next_id = "OEB" + schema + community + "t" + numpy.base_repr(new_code, 36).zfill(6)
        else:
            next_id = "OEB" + schema + community + numpy.base_repr(new_code, 36).zfill(7)

        last_used = numpy.base_repr(new_code, 36).zfill(7)
        return next_id, str(last_used)