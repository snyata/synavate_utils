 def test_successful_message_delivery(self):
        class MockMessage:
            def topic(self):
                return "test_topic"
        
            def partition(self):
                return 0
    
        msg = MockMessage()
        err = None
        delivery_report(err, msg)

def test_failed_message_delivery(self):
        err = "Network error"
        msg = None
        delivery_report(err, msg)