import unittest
from datetime import datetime
from ticket_booking_centre import TicketBookingCentre, Customer, Counter


class TicketBookingCentreTestCase(unittest.TestCase):

    def test_simulate_ticket_booking(self):
        booking_centre = TicketBookingCentre(2, 4, 30, [datetime(2000, 1, 1, 8, 0, 0), datetime(2000, 1, 1, 8, 30, 0)])
        queue_stream = [
            [datetime(2000, 1, 1, 8, 0, 0), "P1", 1],
            [datetime(2000, 1, 1, 8, 1, 0), "P2", 4],
            [datetime(2000, 1, 1, 8, 1, 40), "P3", 1],
            [datetime(2000, 1, 1, 8, 3, 0), "P4", 1],
            [datetime(2000, 1, 1, 8, 3, 0), "P5", 1],
            [datetime(2000, 1, 1, 8, 3, 30), "P6", 1]
        ]
        booking_centre.simulate_ticket_booking(queue_stream)
        self.assertCountEqual([c.customer_id for c in filter(lambda x: x.tickets_booked > 0, booking_centre.customers)],
                         ["P1", "P2", "P3", "P4", "P5"])
        self.assertCountEqual([c.customer_id for c in filter(lambda x: x.tickets_booked == 0, booking_centre.customers)], ["P6"])



if __name__ == '__main__':
    unittest.main()