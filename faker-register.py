import psycopg2
from faker import Faker
import random
import string
import json
import time
from datetime import datetime
import pandas as pd


globalConnection = None
patientId = None
somatometryId = None
medicalUnitId = 301
employeeId = 441
appointmentId = None
healthcareTypePatientId = None
prescriptionId = None
diagCIEPatientId = None
referenceId = None
medicalRecordId = None
referenceBackId = None
medicalNoteId = None
socioeEconomicFileiId = None
triageId = None
hospitalServiceId = None
socialWorrkMentalHealthId = None
fieleEntitiesId = None
medicalHistoryId = None
detectionId = None
familyPlanningId = None

def save_entities_ids():
    global_variables = {
    'patientId': patientId,
    'somatometryId':somatometryId,
    'medicalUnitId':medicalUnitId,
    'employeeId':employeeId,
    'appointmentId':appointmentId,
    'healthcareTypePatientId':healthcareTypePatientId,
    'prescriptionId':prescriptionId,
    'diagCIEPatientId':diagCIEPatientId,
    'referenceId':referenceId,
    'medicalRecordId':medicalRecordId,
    'referenceBackId':referenceBackId,
    'medicalNoteId':medicalNoteId,
    'socioeEconomicFileiId':socioeEconomicFileiId,
    'triageId':triageId,
    'hospitalServiceId':hospitalServiceId,
    'socialWorrkMentalHealthId':socialWorrkMentalHealthId,
    'fieleEntitiesId':fieleEntitiesId,
    'medicalHistoryId':medicalHistoryId,
    'detectionId':detectionId,
    'familyPlanningId':familyPlanningId,
    }

    df = pd.DataFrame(list(global_variables.items()), columns=['Variable', 'Valor'])

    df.to_excel('variables_globales.xlsx', index=False)
def execute_query(query, data,name):
    global globalConnection

    try:
        cursor = globalConnection.cursor()
        cursor.execute(query, data)
        id = cursor.fetchone()[0]
        globalConnection.commit()
        print('Registrado correctamente',name,id)
        return id

    except Exception as error:
        print('query3',name, error)
        return(f"Error: {error}")

def connect():
    global globalConnection
    try:
        host = 'localhost'
        database = 'aurora-health'
        user = 'postgres'
        password = 'postgrespw'

        globalConnection = psycopg2.connect(host=host, database=database, user=user, password=password)
        print("Conexión establecida correctamente.")

    except Exception as error:
        print(f"Error al establecer la conexión: {error}")

def close_connection():
    global globalConnection
    if globalConnection:
        globalConnection.close()
        print("Conexión cerrada.")

def inserts():
    generate_patient()
    generate_somatometry()
    generate_appointment()
    generate_healthcareTypes_Patients()
    generate_prescription()
    generate_diagCIE_patient()
    generate_references()
    generate_medical_records()
    generate_references_back()
    generate_medical_notes()
    generate_socioeconomic_file()
    generate_triage()
    generate_consult()
    generate_hospital_services()
    generate_social_work_mental_healths()
    generate_file_entities()
    #generate_sales_operations()
    generate_medical_histories()
    generate_detection()
    generate_family_planning()
    #save_entities_ids()

def get_timeStamp():
    actualHour = datetime.utcnow()
    myFormat = "%Y-%m-%d %H:%M:%S.%f%z"
    return actualHour.strftime(myFormat)

#! Done
def generate_patient():
    global patientId
    fake = Faker()
    sexuality = ['1', '2']
    query = """
                INSERT INTO public."tblPatients"(
                    "Patient_isAutomaticFileFolio",
                    "Patient_strName",
                    "Patient_strLastName",
                    "Patient_strSurname",
                    "Patient_dtmBirthday",
                    "Patient_intAge",
                    "Patient_isApproximateDate",
                    "Patient_enumSexuality",
                    "Patient_strCURP",
                    "Patient_strChecker",
                    "Patient_isGenericCURP",
                    "Patient_enumMigrant",
                    "Patient_enumIndigenous",
                    "Patient_isApply",
                    "Patient_enumReadAndWrite",
                    "Patient_isForeign",
                    "Patient_isC.P.isIgnored",
                    "Patient_enumAfro-Mexican",
                    "Patient_isSuburdNotFound",
                    "Patient_enumReasonForDeregistration"
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                 RETURNING \"tblPatients\".\"Patient_intId\"
            """
    data = (
            'False',
             fake.name().upper(),
             fake.last_name().upper(),
             #fake.last_name(),
             'UNIFICATIONTEST',
             fake.date_of_birth(minimum_age=1, maximum_age=80),
             '99',
            'False',
             fake.random_element(sexuality),
            'XXXX777777XXXXXX',
            77,
            'True',
            '0',
            '0',
            'False',
            '1',
            'False',
            'True',            
            '0',     
            'False',
            'N/A',
    )
    patientId = execute_query(query, data, 'patient');

#! Done
def generate_somatometry():
    global somatometryId
    global patientId
    global medicalUnitId

    jsonData = {"Somatometry_intIMC": 1,  "Somatometry_intSize": 1,  "Somatometry_intWeight": 1,  "Somatometry_intFasting": 1,  "Somatometry_intGlucose": 1,  "Somatometry_intHeartRate": 1,  "Somatometry_intTemperature": 1,  "Somatometry_intBreathingRate": 1,  "Somatometry_intAbdominalGirth": 1,  "Somatometry_foMeanBloodPressure": 1,  "Somatometry_intOxygenSaturation": 1,  "Somatometry_intSystolicPressure": 1,  "Somatometry_intDiastolicPressure": 1,  "Somatometry_intHeadCircumference": 1}
    query = """INSERT INTO
                public."tblTransSomatometry"(
                        "Somatometry_dtmCreationDate",
                        "Somatometry_jsonSomatometryForm",
                        "Somatometry_entType",
                        "MedicalUnit_intCode",
                        "Patient_intId",
                        "Employee_intId",
                        "Somatometry_enumStatus",
                        "Somatometry_dtmDate"
                    ) 
                VALUES
                    ( %s, %s, %s, %s, %s, %s, %s, %s) 
                RETURNING \"tblTransSomatometry\".\"Somatometry_bntId\"
            """
    data = (
        get_timeStamp(),
        json.dumps(jsonData),
        'Consult',
        medicalUnitId,
        patientId,
        '1',
        '2',
        get_timeStamp()
    )
    somatometryId = execute_query(query, data, 'somatometry');

#! Done
def generate_appointment():
    global employeeId
    global patientId
    global medicalUnitId
    global appointmentId

    query ="""INSERT INTO
                public."tblTransAppointments"(
                    "Appointment_dtmDate",
                    "Appointment_isSpecial",
                    "Appointment_isForeing",
                    "Appointment_strComments",
                    "MedicalOffice_intId",
                    "Employee_intId",
                    "Patient_intId",
                    "MedicalUnit_intId",
                    "Appointment_enumType",
                    "Appointment_strStatusConsult",
                    "Appointment_dtmCreatedAt",
                    "Appointment_entType",
                    "Appointment_strStatus"
                )
            VALUES
                ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING \"tblTransAppointments\".\"Appointment_bntId\"
            """
    data = (
            get_timeStamp(),
            'False',
            'False',
            'registro para test',
            '18',
            employeeId,
            patientId,
            medicalUnitId,
            '1',
            'A',
            get_timeStamp(),
            'tblTransAppointments_Level1',
            'A'
           )
    
    appointmentId = execute_query(query, data, 'appointment');

#! Done
def generate_healthcareTypes_Patients():
    global patientId
    global healthcareTypePatientId

    query = """INSERT INTO
                public."tblHealthcareTypes_Patients"(
                    "HealthcareType_strHealthcareAffiliationNumber",
                    "HealthcareType_dtmHealtcareExpDate",
                    "HealthcareType_intSequence",
                    "Patient_isGratuity",
                    "HealthcareType_intId",
                    "Patient_intId",
                    "HealthcareTypePatient_isPrincipal"
                )
            VALUES
                (%s,%s,%s,%s,%s,%s,%s)
            RETURNING \"tblHealthcareTypes_Patients\".\"HealthcareTypePatient_bntId\""""
    data = (
            random.randrange(10**11, 10**12),
            get_timeStamp(),
            1,
            'True',
            1,
            patientId,
            'False'
        )
    healthcareTypePatientId = execute_query(query, data, 'healthcareTypePatient');

#! Done
def generate_prescription():
    global prescriptionId
    global patientId
    global employeeId

    query = """INSERT INTO
                public."tblTransPrescription"(
                    "Prescription_jsonPrescriptionForm",
                    "Prescription_dtmCreatedAt",
                    "Prescription_entType",
                    "Patient_intId",
                    "Employee_intId",
                    "Prescription_strFolio",
                    "TransPrescription_dtmExpiredDate",
                    "TransPrescription_strPharmacySupplierFullName",
                    "TransPrescription_enumStatus",
                    "TransPrescription_enumSourceChannel"
                )
            VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING \"tblTransPrescription\".\"Prescription_bntId\"
            """
    
    jsonData = {"locCity_bntId": 999999,"medicalUnit_bntId": 104,"prescription_intAge": 28,"prescription_strDate": "2023-01-01","prescription_isSexuality": True,"prescription_intImpression": 0,"prescription_strFileNumber": "ASD7845 ","prescription_intJurisdiction": 4,"prescription_strNameOfPatient": "1",	"prescription_intValidityOfRights": 0,"prescription_strAffiliationNumber": "12345A","prescription_intCauseInterventionNumber": 1}
    data = (
                json.dumps(jsonData),
                get_timeStamp(),
                'Consult',
                patientId,
                employeeId,
                'TESTUNIFICATION' + str(random.randint(0, 99999999)).zfill(8),
                get_timeStamp() ,
                'TEST DE UNIFICACIÓN',
                'PENDING',
                'WEB'
            )
    
    prescriptionId = execute_query(query, data, 'prescription');

#! Done
def generate_diagCIE_patient():
    global patientId
    global diagCIEPatientId
    query = """INSERT INTO
                    public."tblDiagCIE_Patients"(
                        "Patient_intId",
                        "DiagCIE_intId"
                    )
                VALUES
                    (%s,%s)
                RETURNING \"tblDiagCIE_Patients\".\"DiagCIEPatient_bntId\"
            """
    data = (
            patientId,
           '14511'
           )

    diagCIEPatientId = execute_query(query, data,'diagCIEPatient');

#! Done
def generate_references():
    global referenceId
    global patientId
    global employeeId

    query = """INSERT INTO
                public."tblTransReferences"(
                    "Reference_jsonReferenceForm",
                    "Reference_dtmCreatedAt",
                    "Reference_entType",
                    "Patient_intId",
                    "Employee_intId",
                    "Reference_enumStatus",
                    "MedicalUnit_intIdOrigin"
                )
            VALUES
                (%s,%s,%s,%s,%s,%s,%s) 
            RETURNING \"tblTransReferences\".\"Reference_bntId\"
            """
    jsonData = {"DiagCIE": 35,	"Service": 10,	"Specialty": 1,	"MedicalUnit": 237,	"ReasonForShipment": 9,	"Reference_isUrgency": False,	"Reference_intSilverman": 0,	"Reference_strEvolution": "1",	"Reference_intGlasgowScale": 0,	"Reference_strRelationship": "1",	"Reference_strControlNumber": "",	"Reference_enumTypeofPatient": "test",	"Reference_strCurrentCondition": "1",	"Reference_strDiagnosticImpression": "1","Reference_isReferralForCancerUnder18": False,"Reference_strPhysicianAcceptingReferral": "1",	"Reference_strLaboratoryAndCabinetStudies": "1","Reference_enumSocioeconomicClassification": "1","Reference_strNameOfTheRelativeOrPersonResponsible": "1"  }
    
    data = (
        json.dumps(jsonData),
        get_timeStamp(),
        'Consult',
        patientId,
        employeeId,
        'ON_HOLD',
        301,
    )

    referenceId = execute_query(query, data, 'reference');

#! Done
def generate_medical_records():
    global medicalRecordId
    global patientId
    global medicalUnitId
    query = """INSERT INTO
                public."tblTransMedicalRecords"(
                    "MedicalRecord_strFileNumber",
                    "Patient_intId",
                    "MedicalUnit_intId",
                    "MedicalRecord_strStatusTRIAGE",
                    "MedicalRecord_dtmCreatedAt",
                    "MedicalRecord_isAdmissionEmergency",
                    "MedicalRecord_enumUnificationStatus"
                )
            VALUES
                (%s,%s,%s,%s,%s,%s,%s)
            RETURNING \"tblTransMedicalRecords\".\"MedicalRecord_intId\"
            """
    data = (
        str(patientId)+'_UTEST_'+str(medicalUnitId),
        patientId,
        medicalUnitId,
        'G',
        get_timeStamp(),
        'False',
        'N/A',
    )
    
    medicalRecordId = execute_query(query, data, 'medicalRecord');

#! Done
def generate_references_back():
    global referenceBackId
    global patientId
    global employeeId
    query = """INSERT INTO
                public."tblTransReferencesBack"(
                    "ReferencesBack_dtmCreatedAt",
                    "Reference_jsonReferenceForm",
                    "ReferenceBack_entType",
                    "MedicalUnit_intIdOrigin",
                    "Patient_intId",
                    "Employee_intId"
                )
            VALUES
                (%s,%s,%s,%s,%s,%s)
            RETURNING \"tblTransReferencesBack\".\"ReferenceBack_bntId\"
            """
    jsonData = {"Service": 135,"MedicalUnit": 54964,"ReferenceBack_strFolio": "2312U1044044025-C","ReferenceBack_strResumen": "2",	"ReferenceBack_strExitDiagnosis": "5",	"ReferenceBack_strEntryDiagnosis": "4",	"ReferenceBack_strCurrentCondition": "1",	"ReferenceBack_strLaboratoryAndCabinetStudies": "3","ReferenceBack_strInstructionandRecommendations": "6"}
    data = (
            get_timeStamp(),
            json.dumps(jsonData),
            'Consult',
            301,
            patientId,
            employeeId        
            )

    referenceBackId = execute_query(query, data, 'referenceBack');

#! Done
def generate_medical_notes():
    global medicalNoteId
    global patientId
    global employeeId
    global medicalUnitId
    global somatometryId

    query = """INSERT INTO
                public."tblTransMedicalNotes"(
                    "MedicalNote_jsonMedicalNoteForm",
                    "MedicalNote_dtmCreatedAt",
                    "MedicalNote_entType",
                    "Patient_intId",
                    "Employee_intId",
                    "MedicalUnit_intId",
                    "Somatometry_bntId",
                    "MedicalNote_enumStatus",
                    "MedicalNote_dtmDate"
                )
            VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s) 
            RETURNING \"tblTransMedicalNotes\".\"MedicalNote_bntId\"
            """
    jsonData = '{"medicalNote_strDescription": "nota del medico"}'
    data = (
                json.dumps(jsonData),
                get_timeStamp(),
                'Consult',
                patientId,
                employeeId,
                medicalUnitId,
                somatometryId,
                '2' ,
                get_timeStamp()
            )
    medicalNoteId = execute_query(query, data,'medicalNote');

#! Done
def generate_socioeconomic_file():
    global socioeEconomicFileiId
    global patientId
    global employeeId

    query = """INSERT INTO
                public."tblTransSocioeconomicFile"(
                    "SocioeconomicFile_jsonForm",
                    "Patient_intId",
                    "Employee_intId"
                )
            VALUES
                (%s,%s,%s)
            RETURNING \"tblTransSocioeconomicFile\".\"SocioeconomicFile_bntId\"
            """

    jsonData = {"SocioeconomicFile_intAge": 33,	"SocioeconomicFile_dtmDate": "2023-06-23","SocioeconomicFile_intBedNumber": 44,	"SocioeconomicFile_enumReference": "N",	"SocioeconomicFile_intFileNumber": 3543,"SocioeconomicFile_strFamilyName": "JUAN",	"SocioeconomicFile_intFamilyPhone": 3454654576,	"SocioeconomicFile_strRelationship": "PRIMO",	"SocioeconomicFile_intProductionTime": "11:40",	"SocioeconomicFile_strAscriptionUnit": "TEXT",	"SocioeconomicFile_dtmDateOfAdmission": "2023-05-31","SocioeconomicFile_dtmDateOfElaboration": "2023-05-23","SocioeconomicFile_enumLegalMedicalCase": "N","SocioeconomicFile_enumSocioeconomicLevel": "2"}
    data = (
        json.dumps(jsonData),
        patientId,
        employeeId,
    )
    socioeEconomicFileiId = execute_query(query, data,'socioeEconomicFile');

#! Done
def generate_triage():
    global triageId
    global patientId
    global employeeId
    global medicalUnitId

    query = """INSERT INTO
                public."tblTransTriage"(
                    "Triage_intAssignedTurn",
                    "Triage_strReasonForAttention",
                    "Triage_enumStatusTriage",
                    "Patient_intId",
                    "Employee_intIdCreateBy",
                    "MedicalUnit_intId",
                    "Triage_dtmCreateAt"  
                )
            VALUES
                (%s,%s,%s,%s,%s,%s,%s) 
            RETURNING \"tblTransTriage\".\"Triage_bntId\"
            """
    data = (
         999 ,
        'unificación test',
        'ACTIVE',
        patientId,
        employeeId,
        medicalUnitId,
        get_timeStamp(),        
        )
    triageId = execute_query(query, data,'triage');

#! Done
def generate_consult():
    global consultId
    global patientId
    global appointmentId
    global medicalNoteId
    global somatometryId

    query = """INSERT INTO
                public."tblTransConsults"(
                    "Consult_dtmCreatedAt",
                    "Patient_intId",
                    "Appointment_bntId",
                    "Employee_intId",
                    "MedicalUnit_intId",
                    "MedicalNote_bntId",
                    "Somatometry_bntId",		
                    "Consult_dtmDateConsult"
                )
            VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING \"tblTransConsults\".\"Consult_bntId\"
            """
    data =(
                get_timeStamp(),
                patientId,
                appointmentId,
                1,
                301,
                medicalNoteId,
                somatometryId,
                get_timeStamp(),
            )
    consultId = execute_query(query, data,'consult');

#! Done
def generate_hospital_services():
    global hospitalServiceId
    global patientId
    global employeeId
    global medicalUnitId
    query = """INSERT INTO
                public."tblTransHospitalServices"(
                    "HospitalService_jsonForm",
                    "Patient_intId",
                    "Employee_intIdCreatedBy",
                    "MedicalUnit_intId",
                    "Employee_intIdResponsible",
                    "HealthService_dtmCreatedAt",
                    "HospitalServices_entType",
                    "Employee_intIdValidator"
                )
            VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING \"tblTransHospitalServices\".\"HospitalService_bntId\"
            """

    jsonData = {"UrgencyStay_enumStatus": "I","UrgencyStay_enumTypeBed": 1,"MedicalUnit_intIdDestiny": {},"UrgencyStay_dtmDateEntry": "2023-06-10",	"UrgencyStay_strEntryTime": "10:43","MedicalUnit_intIdReferred": {},	"DiagCIE_intIdMainCondition": {},	"UrgencyStay_enumTypeUrgency": 2,	"UrgencyStay_strDischargeDate": "2023-06-10",	"UrgencyStay_strDischargeTime": "10:43",	"UrgencyStay_enumPrehospitalCare": "2",	"UrgencyStay_enumReasonAttention": 2,"UrgencyStay_enumReasonDischange": 2,"UrgencyStay_enumTemporaryTransfer": "2",	"UrgencyStay_strDescriptionMainCondition": "urgencia no calificada"}
    data = (
        json.dumps(jsonData),
        patientId,
        employeeId,
        medicalUnitId,
        employeeId,
        get_timeStamp(),
        'HospitalStays',
        employeeId,
    )
    hospitalServiceId = execute_query(query, data,'hospitalService');

#! 
def generate_sales_operations(patientId, employeeId, medicalUnitId):
    fake = Faker()
    json = '{ "SocialWorkMentalHealth_enumSocialManagement": "3", "SocialWorkMentalHealth_enumReasonForHomeVisit": "2", "SocialWorkMentalHealth_enumRecordIdentification": "2"}'
    salesOperation = {
        "SocialWorkMentalHealth_jsonDetectionForm":json,
        "Patient_intId": patientId,
        "Employee_intId": employeeId,
        "MedicalUnit_intId": medicalUnitId,
        "SocialWorkMentalHealth_dtmCreatedAt": fake.date_time(),
    }
    return salesOperation

#! Done
def generate_social_work_mental_healths():
    global socialWorrkMentalHealthId
    global patientId
    global employeeId
    global medicalUnitId
    query = """INSERT INTO
                public."tblTransSocialWorkMentalHealths"(
                    "SocialWorkMentalHealth_jsonDetectionForm",
                    "Patient_intId",
                    "Employee_intId",
                    "MedicalUnit_intId",
                    "SocialWorkMentalHealth_dtmCreatedAt"
                )
            VALUES
                (%s,%s,%s,%s,%s) 
            RETURNING \"tblTransSocialWorkMentalHealths\".\"SocialWorkMentalHealth_bntId\"
            """
    jsonData = '{"SocialWorkMentalHealth_enumSocialManagement": "3","SocialWorkMentalHealth_enumReasonForHomeVisit": "2", "SocialWorkMentalHealth_enumRecordIdentification": "2"}'
    data = (
        json.dumps(jsonData),
        patientId,
        employeeId,
        medicalUnitId,
        get_timeStamp(),
    )
    socialWorrkMentalHealthId = execute_query(query, data,'socialWorrkMentalHealth');

#! Done
def generate_file_entities():
    global fieleEntitiesId
    global employeeId
    global patientId
    global medicalUnitId
    query = """INSERT INTO
                public."tblFilesEntities"(
                    "FileEntity_entType",
                    "Employee_intId",
                    "MedicalUnit_intId",
                    "Patient_intId",
                    "FileEntities_strName",
                    "FileStorage_bntId",
                    "EmployeeRegistered_intId",
                    "FileEntities_dtmCreatedAt"
                )
            VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING \"tblFilesEntities\".\"FileEntities_bntId\"
            """
    data = (
        'Patient',
        employeeId,
        medicalUnitId,
        patientId,
        'test unificacion',
        48, #?
        employeeId,
        get_timeStamp(),
    )
    fieleEntitiesId = execute_query(query, data,'fieleEntities');

#! Done
def generate_medical_histories():
    global medicalHistoryId
    global employeeId
    global medicalUnitId
    global consultId
    query = """INSERT INTO
                public."tblTransMedicalHistories"(
                    "MedicalHistory_dtmCreatedAt",
                    "MedicalHistory_txtMedicalHistoryNote",
                    "Patient_intId",
                    "Employee_intId",
                    "Consult_bntId",
                    "MedicalUnit_intId"
                )
            VALUES
                (%s,%s,%s,%s,%s,%s)
            RETURNING \"tblTransMedicalHistories\".\"MedicalHistory_btnId\"
            """
    data = (
        get_timeStamp(),
        'Nota medica pata test',
        patientId,
        employeeId,
        consultId,
        medicalUnitId
    )
    medicalHistoryId = execute_query(query, data,'medicalHistory');

#! Done
def generate_detection( ):
    global detectionId
    global employeeId
    global medicalUnitId
    global consultId
    global somatometryId

    query = """INSERT INTO
                public."tblDetections"(
                    "Detection_jsonDetectionForm",
                    "Patient_intId",
                    "MedicalUnit_intId",
                    "Employee_intId",
                    "ServiceConsultType_intId",
                    "Consult_intId",
                    "Somatometry_bntId",
                    "FamilyPlanning_dtmCreatedAt",
                    "Detection_dtmDate",
                    "Employee_intCreatedBy"		
                )
            VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
            RETURNING \"tblDetections\".\"Detection_bntId\"
            """
    jsonData ='{"Detection_enumVIH": "-1",	"Detection_isCode100": false,	"Detection_isOftenSad": "-1",	"Detection_enumAlcohol": "-1",	"Detection_enumAnxiety": "-1",	"Detection_enumCocaine": "-1",	"Detection_enumObesity": "-1",	"Detection_enumOpiates": "-1",	"Detection_enumTestVPH": "-1",	"Detection_enumTobacco": "-1",	"Detection_enumCannabis": "-1",	"Detection_enumSyphilis": "-1",	"Detection_isHealthCard": false,	"Detection_enumChlamydia": null,	"Detection_enumGonorrhea": "-1",	"Detection_enumLevelRisk": null,	"Detection_enumResultVPH": "-1",	"Detection_enumDepression": "-1",	"Detection_enumHepatitisB": null,	"Detection_enumHepatitisC": "-1",	"Detection_enumInhalables": "-1",	"Detection_enumMethodUsed": null,	"Detection_isSuicidalRisk": false,	"Detection_enumTumorousITS": "-1",	"Detection_enumSecretoryITS": "-1",	"Detection_dateDetectionDate": "2023-05-20",	"Detection_enumCaregiversAge": "1",	"Detection_enumDyslipidemias": "-1",	"Detection_enumHallucinogens": "-1",	"Detection_enumHenitalHerpes": null,	"Detection_enumTranquilizers": "-1",	"Detection_enumUlcerativeITS": "-1",	"Detection_intEvaluationABVD": null,	"Detection_intEvaluationAIVD": null,	"Detection_intDetectionStrips": null,	"Detection_enumOtherSubstances": "-1",	"Detection_isAttemptedSuicides": false,	"Detection_enumHepatitisCResult": "-1",	"Detection_enumMellitusDiabetes": "-1",	"Detection_enumMethamphetamines": "-1",	"Detection_enumCervicalCancerTest": "-1",	"Detection_enumGonorrheaDetections": null,	"Detection_intPatientControlStrips": null,	"Detection_enumArterialHypertension": "-1",	"Detection_enumCervicalCancerResult": null,	"Detection_enumHepatitisCDetections": null,	"Detection_enumSpirometryTestResult": "-1",	"Detection_intHealthyPregnantStrips": null,	"Detection_intSpirometryResult_VEF1": null,	"Detection_enumTBRespiratorySymptoms": "-1",	"Detection_enumFamilyViolence10AndOver": "-1",	"Detection_enumNumberAttemptedSuicides": null,	"Detection_enumSuspectedTurnerSyndrome": "-1",	"Detection_intProstaticAntigenReagents": null,	"Detection_intSpirometryResultVEF1_CVF": null,	"Detection_enumA539IncludesPregnantWomen": null,	"Detection_enumB24xIncludesPregnantWomen": null,	"Detection_isIntegratedLifeLineConsultation": false,	"Detection_enumBreastCancerClinicalExamination": "-1",	"Detection_enumProstaticHyerlapsiaInMenAged45AndOver": "-1"}'
    data = (
        json.dumps(jsonData),
        patientId,
        medicalUnitId,
        employeeId,
        1,
        consultId,
        somatometryId,
        get_timeStamp(),
        get_timeStamp(),
        employeeId,
    )
    detectionId = execute_query(query, data,'detection');

#! Done
def generate_family_planning():
    global familyPlanningId
    global employeeId
    global medicalUnitId
    global consultId
    global somatometryId

    query = """INSERT INTO
                public."tblTransConsults_FamilyPlanning"(
                    "FamilyPlanning_jsonForm",
                    "Patient_intId",
                    "MedicalUnit_intId",
                    "Employee_intId",
                    "Employee_intCreatedBy",
                    "ServiceConsultType_intId",
                    "Somatometry_bntId",
                    "FamilyPlanning_dtmCreatedAt",
                    "Consult_intId"
                )
            VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING \"tblTransConsults_FamilyPlanning\".\"FamilyPlanning_bntId\" 
            """
    jsonData = '{"FamilyPlanning_enumDiu": "0",	"FamilyPlanning_intOral": 0,"FamilyPlanning_intDermalPatch": 0,	"FamilyPlanning_enumOtherMethod": 0,	"FamilyPlanning_intFemaleCondom": 0,"FamilyPlanning_intPreservative": 1,"FamilyPlanning_enumMedicatedDIU": "-1","FamilyPlanning_isFamilyPlanning": false,"FamilyPlanning_enumSurgicalMethod": "0",	"FamilyPlanning_isPreventionsOfITS": false,	"FamilyPlanning_enumSubdermicImplant": "-1","FamilyPlanning_intMonthlyInjectable": 0,"FamilyPlanning_isAcceptingPuerperium": false,	"FamilyPlanning_isPregnancyPrevention": false,	"FamilyPlanning_intInjectableBimonthly": 0,	"FamilyPlanning_intQuarterlyInjectable": 0,	"FamilyPlanning_isOtherAttentionsOfSSRA": false,	"FamilyPlanning_enumEmergencyContraception": "0",	"FamilyPlanning_enumPuerperalFamilyPlanning": "-1",	"FamilyPlanning_enumVasectomyWithoutScalpel": "-1",	"FamilyPlanning_enumDischargeWithAzoospermia": "0",	"FamilyPlanning_enumFamilyPlanningCounseling": "0"}'
    data = (
        json.dumps(jsonData),
        patientId,
        medicalUnitId,
        employeeId,
        employeeId,
        1,
        somatometryId,
        get_timeStamp(),
        consultId,
    )
    familyPlanningId = execute_query(query, data,'familyPlanning');

if __name__ == "__main__":
    connect()
    inserts()
    close_connection()
