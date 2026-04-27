class SessionSummary:

    @staticmethod
    def display(summary):

        print("\n====== SESSION SUMMARY ======")

        for key, value in summary.items():
            print(f"{key}: {value}")

        print("=============================\n")