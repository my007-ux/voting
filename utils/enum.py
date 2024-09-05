class Types:
    def get_user_type(self, user_type):
        """Returns a random key for given type."""

        user_type_dict = {'Organization Admin': 1, 'Hotel Admin': 2, 'Account Manager':3, 'Front Desk':4,'Staff':5}
        if type(user_type).__name__ == 'int':
            for key, value in user_type_dict.items():
                if value == user_type:
                    return key
        if user_type_dict.get(user_type):
            return user_type_dict[user_type]
        return 0

    def get_integration_type(self, integration_type):
        """Returns a random key for given type."""

        integration_type_dict = {'API': 1, 'OAUTH': 2}
        if type(integration_type).__name__ == 'int':
            for key, value in integration_type_dict.items():
                if value == integration_type:
                    return key
        if integration_type_dict.get(integration_type):
            return integration_type_dict[integration_type]
        return 0

    def get_integration_detail_status(self, integration_detail_status):
        """Returns a random key for given type."""

        integration_detail_status_dict = {'Active': 1, 'Pending': 2, 'Error': 3, 'Deleted': 4}
        if type(integration_detail_status).__name__ == 'int':
            for key, value in integration_detail_status_dict.items():
                if value == integration_detail_status:
                    return key
        if integration_detail_status_dict.get(integration_detail_status):
            return integration_detail_status_dict[integration_detail_status]
        return 0

    def get_status(self, status):

        status_dict = {'pending': 1, 'active': 2, 'deactivate': 3, 'deleted': 4}
        if type(status).__name__ == 'int':
            for key, value in status_dict.items():
                if value == status:
                    return key

        if status_dict.get(status):
            return status_dict[status]
        return 0

    def get_priority(self, priority):
        priority_dict = {'low': 1, 'medium': 2, 'high': 3}
        if type(priority).__name__ == 'int':
            for key, value in priority_dict.items():
                if value == priority:
                    return key
        if priority_dict.get(priority):
            return priority_dict[priority]

        return None

    def get_uploaded_file_status(self, status):
        status_dict = {'processing': 1, 'done': 2, 'error occurred': 3, 'Delete': 4, 'invalid': 5}
        if type(status).__name__ == 'int':
            for key, value in status_dict.items():
                if value == status:
                    return key

        if status_dict.get(status):
            return status_dict[status]
        return 0

    def get_document_status(self, status):
        status_dict = {
            'Processing Started': 1,
            'Extracted Answers': 2,
            'Error': 3,
            'delete': 4,
            'Pending Question Review': 5,
            'Extracting Questions': 6,
            'Finalised': 7
        }
        if type(status).__name__ == 'int':
            for key, value in status_dict.items():
                if value == status:
                    return key

        if status_dict.get(status):
            return status_dict[status]
        return 0

    def get_question_status(self, status):
        status_dict = {'Answer Pending': 1, 'Needs Approval': 2, 'Approved': 3, 'Rejected': 4, 'deleted': 5}
        if type(status).__name__ == 'int':
            for key, value in status_dict.items():
                if value == status:
                    return key

        if status_dict.get(status):
            return status_dict[status]
        return 0

    def get_question_source(self, source):
        source_dict = {'File Upload': 1, 'Chrome Extension': 2, 'Spreadsheet': 3}
        if type(source).__name__ == 'int':
            for key, value in source_dict.items():
                if value == source:
                    return key

        if source_dict.get(source):
            return source_dict[source]
        return 0

    def get_pdf_processing_status(self, status):
        status_dict = {'Processing Started': 1, 'Extracted Questions': 2, 'Process Failed': 3}
        if type(status).__name__ == 'int':
            for key, value in status_dict.items():
                if value == status:
                    return key

        if status_dict.get(status):
            return status_dict[status]
        return 0

    def get_question_set_source(self, source):

        source_dict = {'File Manager': 1, 'Chrome Extension': 2, 'Spreadsheet': 3}
        if type(source).__name__ == 'int':
            for key, value in source_dict.items():
                if value == source:
                    return key

        if source_dict.get(source):
            return source_dict[source]
        return 0

    def get_file_tag_status(self, status):
        """Returns a random key for given type."""

        satus_dict = {'Active': 1, 'Deleted': 4}
        if type(status).__name__ == 'int':
            for key, value in satus_dict.items():
                if value == status:
                    return key
        if satus_dict.get(status):
            return satus_dict[status]
        return 0

    def get_commitment_status(self, status):
        status_dict = {'Pending': 1, 'Done': 2, 'Delayed': 3, 'Deleted': 4}
        if type(status).__name__ == 'int':
            for key, value in status_dict.items():
                if value == status:
                    return key

        if status_dict.get(status):
            return status_dict[status]
        return 0

    def get_custom_instruction_status(self, status):
        status_dict = {'Active': 1, 'Deleted': 2}
        if type(status).__name__ == 'int':
            for key, value in status_dict.items():
                if value == status:
                    return key

        if status_dict.get(status):
            return status_dict[status]
        return 0

    def get_spread_sheet_data_status(self, status):
        status_dict = {'Pending': 1, 'Done': 2, 'Error': 3, 'Deleted': 4}
        if type(status).__name__ == 'int':
            for key, value in status_dict.items():
                if value == status:
                    return key

        if status_dict.get(status):
            return status_dict[status]
        return 0
