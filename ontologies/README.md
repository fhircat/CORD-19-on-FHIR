## COVID-19 PICO Ontology
The COVID-19 PICO Ontology (CPICO) is developed as an extension of [Cochrane PICO Ontology](https://linkeddata.cochrane.org/pico-ontology) for supporting COVID-19 evidence extraction and formulating COVID-19 research questions.

The PICO model is widely used and taught in evidence-based health care as a strategy for formulating questions and search strategies and for characterizing clinical studies or meta-analyses . PICO stands for 4 different potential components of a clinical question:

    Patient, Population or Problem
        What are the characteristics of the patient or population (demographics, risk factors, pre-existing conditions, etc)?
        What is the condition or disease of interest?
    Intervention
        What is the intervention under consideration for this patient or population?
    Comparison
        What is the alternative to the intervention (e.g. placebo, different drug, surgery)?
    Outcome
        What are the relevant outcomes (e.g. quality of life, change in clinical status, morbidity, adverse effects, complications)?
        

The CPICO Ontology provides specific subtype definitions for the PICO classes of Population, Intervention, and Outcome. These subtypes came from two sources: 1) Semantic annotations mined from the CORD-19-on-FHIR datasets; and 2) Manual review of COVID-19 articles.

## Population Subtypes - COVID-19 Population
These subtypes include COVID-19 Patients with comorbidities like diabetes and cancer, smoking history, pregnancy, and more.

![COVID-19 Population](https://github.com/fhircat/CORD-19-on-FHIR/blob/master/ontologies/population_substypes.png "COVID-19 Population")



## Intervention Subtypes - COVID-19 Intervention
These subtyeps include COVID-19 Intervention with Medication, Concomitant Medications, and Precedure.

![COVID-19 Population](https://github.com/fhircat/CORD-19-on-FHIR/blob/master/ontologies/intervension_subtypes_01.png "COVID-19 Intervention")

## Outcome Subtypes - COVID-19 Outcome
These subtypes include disease serverity, disease progression, need for ICU hosptializaiton, need for mechanical ventilation, and mortality.

![COVID-19 Outcome](https://github.com/fhircat/CORD-19-on-FHIR/blob/master/ontologies/outcome_subtypes.png "COVID-19 Outcome")

