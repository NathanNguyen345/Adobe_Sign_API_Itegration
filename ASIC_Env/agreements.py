def create_agreement(ID, email):
    agreement = {
        "documentCreationInfo": {
            "fileInfos": [{
                "transientDocumentId": ID
            }],
            "name": "MyTestAgreement",
            "recipientSetInfos": [
                {
                    "recipientSetMemberInfos": [
                        {
                            "email": email,
                            "fax": ""
                        }
                    ],
                    "recipientSetRole": "SIGNER"
                }
            ],
            "signatureType": "ESIGN",
            "signatureFlow": "SENDER_SIGNATURE_NOT_REQUIRED"
        }
    }
    return agreement
