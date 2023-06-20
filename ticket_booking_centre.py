from datetime import  timedelta


class Counter:
    def __init__(self, counter_id, queue_capacity, processing_time):
        self.counter_id = counter_id
        self.count = 0
        self.queue_capacity = queue_capacity
        self.queue = []
        self.status = "closed"
        self.processing_time = processing_time
        self.ticket_processing_end_time = None

    def open_counter(self):
        self.status = "open"

    def close_counter(self):
        self.status = "closed"

    def process_tickets(self):
        if self.queue:
            customer = self.queue.pop(0)
            self.count += 1
            processing_start_time = max(self.ticket_processing_end_time,
                                        customer.enter_time) if self.ticket_processing_end_time else customer.enter_time
            self.ticket_processing_end_time = processing_start_time + timedelta(seconds=self.processing_time)
            print(
                f"Person in the queue: {customer.customer_id} for ticket {customer.tickets_booked + 1}: "
                f"Enters in the Queue at {customer.enter_time} and gets ticket at {self.ticket_processing_end_time} in {self.counter_id}")
            customer.tickets_booked += 1

    def is_queue_full(self):
        return self.count >= self.queue_capacity


class Customer:
    def __init__(self, enter_time, customer_id, required_tickets):
        self.enter_time = enter_time
        self.customer_id = customer_id
        self.total_required_tickets = required_tickets
        self.tickets_booked = 0


class TicketBookingCentre:
    def __init__(self, max_counters, queue_capacity, processing_time, operational_hours):
        self.counters = [Counter(1, queue_capacity, processing_time)]
        self.counters[0].open_counter()
        self.queue_capacity = queue_capacity
        self.operational_hours = operational_hours
        self.processing_time = processing_time
        self.max_counters = max_counters
        self.customers = []

    def add_customer(self, customer):
        min_queue_counter = min(self.counters, key=lambda c: c.count)
        if min_queue_counter.is_queue_full():
            min_queue_counter.close_counter()
            min_queue_counter = self.open_new_counter()
        if min_queue_counter:
            min_queue_counter.queue.append(customer)

    def open_new_counter(self):
        if len(self.counters) < self.max_counters:
            counter_id = len(self.counters) + 1
            new_counter = Counter(counter_id, self.queue_capacity, self.processing_time)
            new_counter.open_counter()
            self.counters.append(new_counter)
            return new_counter

    def simulate_ticket_booking(self, queue_stream):
        start_time = self.operational_hours[0]
        end_time = self.operational_hours[1]
        current_time = start_time

        while current_time < end_time and queue_stream and any(counter.status == "open" for counter in self.counters):
            queue_stream = sorted(queue_stream, key=lambda x: x[0])
            customer_info = queue_stream.pop(0)
            if customer_info[1] not in [i.customer_id for i in self.customers]:

                customer = Customer(customer_info[0], customer_info[1], customer_info[2])
                self.customers.append(customer)
            else:
                customer = list(filter(lambda x: x.customer_id == customer_info[1], self.customers))[0]
                customer.enter_time = current_time

            self.add_customer(customer)

            # Process tickets for open counters until time exceeds the operational hours

            for counter in self.counters:
                if counter.status == "open":
                    counter.process_tickets()
                    if counter.ticket_processing_end_time:
                        current_time = counter.ticket_processing_end_time

                    if customer.tickets_booked < customer.total_required_tickets:
                        queue_stream.append([current_time, customer.customer_id,
                                             customer.total_required_tickets - customer.tickets_booked])

        for counter in self.counters:
            counter.close_counter()



