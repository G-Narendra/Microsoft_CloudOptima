

# **Payment Card Industry Data Security Standard** 

**Requirements and Testing Procedures** 

**Version 4.0.1** 

June 2024 



## **Document Changes** 

|**Date**|**Version**|**Description**|
|---|---|---|
|October 2008|1.2|To introduce PCI DSS v1.2 as “PCI DSS Requirements and Security Assessment Procedures,” eliminating redundancy<br>between documents, and making both general and specific changes from PCI DSS Security Audit Procedures v1.1. For<br>complete information, see PCI Data Security Standard Summary of Changes from PCI DSS Version 1.1 to 1.2.|
|July 2009|1.2.1|Add sentence that was incorrectly deleted between PCI DSS v1.1 and v1.2.|
|||Correct “then” to “than” in testing procedures 6.3.7.a and 6.3.7.b.|
|||Remove grayed-out marking for “in place” and “not in place” columns in testing procedure 6.5.b.|
|||For Compensating Controls Worksheet – Completed Example, correct wording at top of page to say, “Use this worksheet<br>to define compensating controls for any requirement noted as “in place” via compensating controls.”|
|October 2010|2.0|Update and implemented changes from v1.2.1. See PCI DSS – Summary of Changes from PCI DSS Version 1.2.1 to 2.0.|
|November 2013|3.0|Update from v2.0. See PCI DSS – Summary of Changes from PCI DSS Version 2.0 to 3.0.|
|April 2015|3.1|Update from PCI DSS v3.0. See PCI DSS – Summary of Changes from PCI DSS Version 3.0 to 3.1 for details of<br>changes.|
|April 2016|3.2|Update from PCI DSS v3.1. See PCI DSS – Summary of Changes from PCI DSS Version 3.1 to 3.2 for details of<br>changes.|
|May 2018|3.2.1|Update from PCI DSS v3.2. See PCI DSS–Summary of Changes from PCI DSS Version 3.2 to 3.2.1 for details of<br>changes.|
|March 2022|4.0|Rename document title to “Payment Card Industry Data Security Standard: Requirements and Testing Procedures.”<br>Update from PCI DSS v3.2.1. See PCI DSS – Summary of Changes from PCI DSS Version 3.2.1 to 4.0 for details of<br>changes.|
|June 2024|4.0.1|Update from PCI DSS v4.0. See_PCI DSS - Summary of Changes from PCI DSS Version 4.0 to 4.0.1_for details of<br>changes.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page i_ 



## **Contents** 

|**1**<br>**Introduction and PCI Data Security Standard Overview ................................................................................................................................... 1**|
|---|
|**2**<br>**PCI DSS Applicability Information ....................................................................................................................................................................... 4**|
|**3**<br>**Relationship between PCI DSS and PCI SSC Software Standards .................................................................................................................. 7**|
|**4**<br>**Scope of PCI DSS Requirements ......................................................................................................................................................................... 9**|
|**5**<br>**Best Practices for Implementing PCI DSS into Business-as-Usual Processes ............................................................................................ 19**|
|**6**<br>**For Assessors: Sampling for PCI DSS Assessments...................................................................................................................................... 22**|
|**7**<br>**Description of Timeframes Used in PCI DSS Requirements .......................................................................................................................... 25**|
|**8**<br>**Approaches for Implementing and Validating PCI DSS .................................................................................................................................. 28**|
|**9**<br>**Protecting Information About an Entity’s Security Posture ........................................................................................................................... 30**|
|**10** **Testing Methods for PCI DSS Requirements .................................................................................................................................................... 31**|
|**11** **Instructions and Content for Report on Compliance ....................................................................................................................................... 32**|
|**12** **PCI DSS Assessment Process ........................................................................................................................................................................... 33**|
|**13** **Additional References ......................................................................................................................................................................................... 34**|
|**14** **PCI DSS Versions ................................................................................................................................................................................................ 35**|
|**15** **Detailed PCI DSS Requirements and Testing Procedures .............................................................................................................................. 36**|
|Build and Maintain a Secure Network and Systems ............................................................................................................................................. 38|
|Protect Account Data ............................................................................................................................................................................................. 74|
|Maintain a Vulnerability Management Program .................................................................................................................................................. 119|
|Implement Strong Access Control Measures ...................................................................................................................................................... 161|











_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page ii_ 







|Regularly|Monitor and Test Networks ................................................................................................................................................................. 236|
|---|---|
|Maintain a|n Information Security Policy .............................................................................................................................................................. 290|
|**Appendix A**|**Additional PCI DSS Requirements ............................................................................................................................................. 334**|
|**Appendix B**|**Compensating Controls ............................................................................................................................................................... 369**|
|**Appendix C**|**Compensating Controls Worksheet ........................................................................................................................................... 371**|
|**Appendix D**|**Customized Approach ................................................................................................................................................................. 372**|
|**Appendix E**|**Sample Templates to Support Customized Approach ............................................................................................................. 374**|
|**Appendix F**|**Leveraging the PCI Software Security Framework to Support Requirement 6 ..................................................................... 375**|
|**Appendix G**|**PCI DSS Glossary of Terms, Abbreviations, and Acronyms ................................................................................................... 379**|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page iii_ 



## **1 Introduction and PCI Data Security Standard Overview** 

The Payment Card Industry Data Security Standard (PCI DSS) was developed to encourage and enhance payment account data security and facilitate the broad adoption of consistent data security measures globally. PCI DSS provides a baseline of technical and operational requirements designed to protect account data. While specifically designed to focus on environments with payment account data, PCI DSS can also be used to protect against threats and secure other elements in the payment ecosystem. 

Table 1 shows the 12 principal PCI DSS requirements. 

**Table 1. Principal PCI DSS Requirements** 

|**PCI Data**|**Security Standard – High Level Overview**|
|---|---|
|**Build and Maintain a Secure Network and Systems**|**1.**<br>Install and Maintain Network Security Controls.<br>**2.**<br>Apply Secure Configurations to All System Components.|
|**Protect Account Data**|**3.**<br>Protect Stored Account Data.<br>**4.**<br>Protect Cardholder Data with Strong Cryptography During Transmission Over Open,<br>Public Networks.|
|**Maintain a Vulnerability Management Program**|**5.**<br>Protect All Systems and Networks from Malicious Software.<br>**6.**<br>Develop and Maintain Secure Systems and Software.|
|**Implement Strong Access Control Measures**|**7.**<br>Restrict Access to System Components and Cardholder Data by Business Need to Know.<br>**8.**<br>Identify Users and Authenticate Access to System Components.<br>**9.**<br>Restrict Physical Access to Cardholder Data.|
|**Regularly Monitor and Test Networks**|**10.**Log and Monitor All Access to System Components and Cardholder Data.<br>**11.**Test Security of Systems and Networks Regularly.|
|**Maintain an Information Security Policy**|**12.**Support Information Security with Organizational Policies and Programs.|



This document, the Payment Card Industry Data Security Standard Requirements and Testing Procedures, consists of the 12 PCI DSS principal requirements, detailed security requirements, corresponding testing procedures, and other information pertinent to each requirement. The following sections provide detailed guidelines and best practices to assist entities to prepare for, conduct, and report the results of a PCI DSS assessment. The PCI DSS requirements and testing procedures begin on page 43. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 1_ 



PCI DSS comprises a minimum set of requirements for protecting account data and may be enhanced by additional controls and practices to further mitigate risks, and to incorporate local, regional, and sector laws and regulations. Additionally, legislation or regulatory requirements may require specific protection of personal information or other data elements (for example, cardholder name). 

#### **_Limitations_** 

If any of the requirements contained in this standard conflict with country, state, or local laws, the country, state, or local law will apply. 

### **PCI DSS Resources** 

The PCI Security Standards Council (PCI SSC) website (www.pcisecuritystandards.org) provides the following additional resources to assist organizations with their PCI DSS assessments and validations: 

- Document Library, including: 

   - PCI DSS Summary of Changes 

   - PCI DSS Quick Reference Guide 

   - Information Supplements and Guidelines 

   - Prioritized Approach for PCI DSS 

   - Report on Compliance (ROC) Reporting Template and Reporting Instructions 

   - Self-Assessment Questionnaires (SAQs) and SAQ Instructions and Guidelines 

   - Attestations of Compliance _(_ AOCs _)_ 

- Frequently Asked Questions (FAQs) 

- PCI for Small Merchants website 

- PCI training courses and informational webinars 

- List of Qualified Security Assessors (QSAs) and Approved Scanning Vendors (ASVs) 

- Lists of PCI approved devices, applications, and solutions 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 2_ 



There are over 60 guidance documents and information supplements available on the PCI SSC website that provide specific guidance and considerations for PCI DSS. Examples include: 

- Guidance for PCI DSS Scoping and Network Segmentation 

- PCI SSC Cloud Computing Guidelines 

- Multi-Factor Authentication Guidance 

- Third-Party Security Assurance 

- Effective Daily Log Monitoring 

- Penetration Testing Guidance 

**_Note:_** _Information Supplements complement PCI DSS and identify additional considerations and recommendations for meeting PCI DSS requirements. Information Supplements do not supersede, replace, or extend PCI DSS or any of its requirements._ 

- Best Practices for Implementing a Security Awareness Program 

- Best Practices for Maintaining PCI DSS Compliance 

- PCI DSS for Large Organizations 

- Use of SSL/Early TLS and Impact on ASV Scans 

- Use of SSL/Early TLS for POS POI Terminal Connections 

- Tokenization Product Security Guidelines 

- Protecting Telephone-Based Payment Card Data 

Refer to the Document Library at www.pcisecuritystandards.org for information about these and other resources. 

In addition, refer to _Appendix G_ for definitions of PCI DSS terms. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 3_ 



## **2 PCI DSS Applicability Information** 

PCI DSS is intended for all entities that store, process, or transmit cardholder data (CHD) and/or sensitive authentication data (SAD) or could impact the security of the cardholder data and/or sensitive authentication data. This includes all entities involved in payment account processing —including merchants, processors, acquirers, issuers, and other service providers. 

Whether any entity is required to comply with or validate their compliance to PCI DSS is at the discretion of those organizations that manage compliance programs (such as payment brands and acquirers); contact these organizations for any additional criteria. 

### **Defining Account Data, Cardholder Data, and Sensitive Authentication Data** 

Cardholder data and sensitive authentication data are considered account data and are defined as follows: 

**Table 2. Account Data** 

- **Account Data** 

- **Cardholder Data includes: Sensitive Authentication Data includes:** 

- • Primary Account Number (PAN) • Full track data (magnetic-stripe data or equivalent on a chip) • Cardholder Name • Card verification code • Expiration Date • PINs/PIN blocks • Service Code 

PCI DSS requirements apply to entities with environments where account data (cardholder data and/or sensitive authentication data) is stored, processed, or transmitted, and entities with environments that can impact the security of cardholder data and/or sensitive authentication data. Some PCI DSS requirements may also apply to entities with environments that do not store, process, or transmit account datafor example, entities that outsource payment operations or management of their cardholder data environment (CDE)<sup>1</sup> . Entities that outsource their payment environments or payment operations to third parties remain responsible for ensuring that the account data is protected by the third party per applicable PCI DSS requirements. 

> 1 In accordance with those organizations that manage compliance programs (such as payment brands and acquirers); entities should contact these organizations <u>for more details.</u> 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 4_ 



The primary account number (PAN) is the defining factor for cardholder data. The term account data therefore covers the following: the full PAN, any other elements of cardholder data that are present with the PAN, and any elements of sensitive authentication data. 

If cardholder name, service code, and/or expiration date are stored, processed, or transmitted with the PAN, or are otherwise present in the CDE, they must be protected in accordance with the PCI DSS requirements applicable to cardholder data. 

If an entity stores, processes, or transmits PAN, then a CDE exists to which PCI DSS requirements will apply. Some requirements may not be applicable, for example if the entity does not store PAN, then the requirements relating to the protection of stored PAN in Requirement 3 will not be applicable to the entity. 

Even if an entity does not store, process, or transmit PAN, some PCI DSS requirements may still apply. Consider the following: 

- If the entity stores SAD, requirements specifically related to SAD storage in Requirement 3 will be applicable. 

- If the entity engages third-party service providers to store, process or transmit PAN on its behalf, requirements related to the management of service providers in Requirement 12 will be applicable. 

- If the entity can impact the security of cardholder data and/or sensitive authentication data because the security of an entity’s infrastructure can affect how cardholder data is processed (for example, via a web server that controls the generation of a payment form or page) some requirements will be applicable. 

- If cardholder data is only present on physical media (for example paper), requirements relating to the security and disposal of physical media in Requirement 9 will be applicable. 

- Requirements related to an incident response plan are applicable to all entities, to ensure that there are procedures to follow in the event of a suspected or actual breach of the confidentiality of cardholder data _._ 

#### **_Use of Account Data, Sensitive Authentication Data, Cardholder Data, and Primary Account Number in PCI DSS_** 

PCI DSS includes requirements that specifically refer to account data, cardholder data, and sensitive authentication data. It is important to note that each of these types of data are different and the terms are not interchangeable. Specific references within requirements to account data, cardholder data, or sensitive authentication data are purposeful, and the requirements apply specifically to the type of data that is referenced. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 5_ 



#### **_Elements of Account Data and Storage Requirements_** 

Table 3 identifies the elements of cardholder and sensitive authentication data, whether storage of each data element is permitted or prohibited, and whether each data element must be rendered unreadable—for example, with strong cryptography—when stored. This table is not exhaustive and is presented to illustrate only how the stated requirements apply to the different data elements. 

##### **Table 3. Account Data Element Storage Requirements** 

||**Data Elements**|**Storage Restrictions**|**Required to Render Stored Data**<br>**Unreadable**|
|---|---|---|---|
|**Cardholder**<br>**Data**|Primary Account Number (PAN)|Storage is kept to a minimum as defined in<br>Requirement 3.2|Yes, as defined in Requirement 3.5|
||Cardholder Name|||
|**t Data**|Service Code|Storage is kept to a minimum as defined in<br>Requirement 3.2 <sup>2</sup>|No|
|**coun**|Expiration Date|||
|**Ac**<br>**Sensitive**<br>|Full Track Data||Yes, data stored until authorization is|
|**Authentication**<br>**Data**|Card verification code<br>PIN/PIN Block|Cannot be stored after authorization as<br>defined in Requirement 3.3.1 <sup>3</sup>|complete must be protected with strong<br>cryptography as defined in Requirement<br>3.3.2|



If PAN is stored with other elements of cardholder data, only the PAN must be rendered unreadable according to PCI DSS Requirement 3.5.1. 

Sensitive authentication data must not be stored after authorization, even if encrypted. This applies even for environments where there is no PAN present. 

2 Where data exists in the same environment as PAN. 

3 Except as permitted for issuers and companies that support issuing services. Requirements for issuers and issuing services are separately defined in <u>Requirement 3.3.3.</u> 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

|_June 2024_<br>_Page 6_|
|---|





## **3 Relationship between PCI DSS and PCI SSC Software Standards** 

PCI SSC supports the use of secure payment software within cardholder data environments (CDE) via the Software Security Framework (SSF), which consists of the Secure Software Standard and the Secure Software Lifecycle (Secure SLC) Standard. Software that is PCI SSC validated and listed provides assurance that the software has been developed using secure practices and has met a defined set of software security requirements. 

The PCI SSC secure software programs include listings of payment software and software vendors that have been validated as meeting the applicable PCI SSC Software Standards. 

- **Validated Software** : Payment software listed on the PCI SSC website as a Validated Payment Application (PA-DSS) or Validated Payment Software (the Secure Software Standard) has been evaluated by a qualified assessor to confirm the software meets the security requirements within that standard. The security requirements in these standards are focused on protecting the integrity and confidentiality of payment transactions and account data. 

- **Qualified Software Vendors** : The Secure SLC Standard defines security requirements for software vendors to integrate secure software development practices throughout the entire software lifecycle. Software vendors that have been validated as meeting the Secure SLC Standard are listed on the PCI SSC website as a Secure SLC Qualified Vendor. 

**_Note:_** _PA-DSS and the related program were retired in October 2022. Refer to the PCI SSC List of Validated Payment Applications for expiry dates for PA-DSS validated applications. Since the expiry date, applications are listed as “Acceptable only for Pre-Existing Deployments.” Whether an entity can continue to use a PA-DSS application with an expired listing is at the discretion of organizations that manage compliance programs (such as payment brands and acquirers); entities should contact these organizations for more details._ 

For more information about the SSF or PA-DSS, refer to the respective Program Guides at www.pcisecuritystandards.org. 

All software that stores, processes, or transmits account data, or that could impact the security of cardholder data and/or sensitive authentication data, is in scope for an entity’s PCI DSS assessment. While the use of validated payment software supports the security of an entity’s CDE, the use of such software does not by itself make an entity PCI DSS compliant. The entity’s PCI DSS assessment should include verification that the software is properly configured and securely implemented to support applicable PCI DSS requirements. Additionally, if PCI-listed payment software has been customized, a more in-depth review will be required during the PCI DSS assessment because the software may no longer be representative of the version that was originally validated. 

Because security threats are constantly evolving, software that is no longer supported by the vendor (for example, identified by the vendor as “end of life”) may not offer the same level of security as supported versions. Entities are strongly encouraged to keep their software current and updated to the latest software versions available. 

Entities that develop their own software are encouraged to refer to PCI SSC’s software security standards and consider the requirements therein as best practices to use in their development environments. Secure payment software implemented in a PCI DSS compliant environment will help minimize the potential for security breaches leading to compromises of account data and fraud. See _Bespoke and Custom Software_ . 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 7_ 



### **Applicability of PCI DSS to Payment Software Vendors** 

PCI DSS may apply to a payment software vendor if the vendor is also a service provider that stores, processes, or transmits account data, or has access to their customers’ account data—for example, in the role of a payment service provider or via remote access to a customer environment. Software vendors to which PCI DSS may be applicable include those offering payment services, as well as cloud service providers offering payment terminals in the cloud, software as a service (SaaS), e-commerce in the cloud, and other cloud payment services. 

### **Bespoke and Custom Software** 

All bespoke and custom software that stores, processes, or transmits account data, or that could impact the security of cardholder data and/or sensitive authentication data, is in scope for an entity’s PCI DSS assessment. 

Bespoke and custom software that has been developed and maintained in accordance with one of PCI SSC’s Software Security Framework standards (the Secure Software Standard or the Secure SLC standard) will support an entity in meeting PCI DSS Requirement 6. 

**_Note:_** _PCI DSS Requirement 6 fully applies to bespoke and custom software that has not been developed and maintained in accordance with one of PCI SSC’s Software Security Framework standards. Entities that use software vendors to develop bespoke or custom software that could impact the security of their cardholder data and/or sensitive authentication data are responsible for ensuring those software vendors develop the software according to PCI DSS Requirement 6._ 

See Appendix F for more details. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 8_ 



## **4 Scope of PCI DSS Requirements** 

PCI DSS requirements apply to: 

- The cardholder data environment (CDE), which is comprised of: 

   - System components, people, and processes that store, process, or transmit cardholder data and/or sensitive authentication data, and, 

   - System components that may not store, process, or transmit CHD/SAD but have unrestricted connectivity to system components that store, process, or transmit CHD/SAD. 

###### **AND** 

- System components, people, and processes that could impact the security of cardholder data and/or sensitive authentication data.<sup>4</sup> 

“System components” include network devices, servers, computing devices, virtual components, cloud components, and software. Examples of system components include but are not limited to: 

- Systems that store, process, or transmit account data (for example, payment terminals, authorization systems, clearing systems, payment middleware systems, payment back-office systems, shopping cart and store front systems, payment gateway/switch systems, fraud monitoring systems). 

- Systems that provide security services (for example, authentication servers, access control servers, security information and event management (SIEM) systems, physical security systems (for example, badge access or CCTV), multi-factor authentication systems, anti-malware systems). 

- Systems that facilitate segmentation (for example, internal network security controls). 

- Systems that could impact the security of account data or the CDE (for example, name resolution, or e-commerce (web) redirection servers). 

- Virtualization components such as virtual machines, virtual switches/routers, virtual appliances, virtual applications/desktops, and hypervisors. 

- Cloud infrastructure and components, both external and on premises, and including instantiations of containers or images, virtual private clouds, cloud-based identity and access management, CDEs residing on premises or in the cloud, service meshes with containerized applications, and container orchestration tools. 

> 4 For additional guidance, refer to _<u>Information Supplement: Guidance for PCI DSS Scoping and Network Segmentation</u>_ <u>on the PCI SSC website.</u> 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 9_ 



- Network components, including but not limited to network security controls, switches, routers, VoIP network devices, wireless access points, network appliances, and other security appliances. 

- Server types, including but not limited to web, application, database, authentication, mail, proxy, Network Time Protocol (NTP), and Domain Name System (DNS). 

- End-user devices, such as computers, laptops, workstations, administrative workstations, tablets, and mobile devices. 

- Printers, and multi-function devices that scan, print, and fax. 

- Storage of account data in any format (for example, paper, data files, audio files, images, and video recordings). 

- Applications, software, and software components, serverless applications, including all purchased, subscribed (for example, Softwareas-a-Service), bespoke and custom software, including internal and external (for example, Internet) applications. 

- Tools, code repositories, and systems that implement software configuration management or for deployment of objects to the CDE or to systems that can impact the CDE. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 10_ 



Figure 1 shows considerations for scoping system components for PCI DSS. 

**Figure 1. Understanding PCI DSS Scoping** 



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 11_ 



### **Annual PCI DSS Scope Confirmation** 

The first step in preparing for a PCI DSS assessment is for the entity to accurately determine the scope of the review. The assessed entity must confirm the accuracy of their PCI DSS scope according to PCI DSS Requirement 12.5.2 by identifying all locations and flows of account data, and identifying all systems that are connected to or, if compromised, could impact the CDE (for example, authentication servers, remote access servers, logging servers) to ensure they are included in the PCI DSS scope. All types of systems and locations should be considered during the scoping process, including backup/recovery sites and fail-over systems. 

The minimum steps for an entity to confirm the accuracy of their PCI DSS scope are specified in PCI DSS Requirement 12.5.2. The entity is expected to retain documentation to show how PCI DSS scope was determined. The documentation is retained for assessor review and for reference during the entity’s next PCI DSS scope confirmation activity. For each PCI DSS assessment, the assessor validates that the entity accurately defined and documented the scope of the assessment. 

**_<mark>Note</mark>_** _<mark>: This annual confirmation of PCI DSS scope is defined at PCI DSS Requirement at 12.5.2 and is an activity expected to be performed by the entity. This activity is not the same, nor is it intended to be replaced by, the scoping confirmation performed by the entity’s assessor during the assessment.</mark>_ 

### **Segmentation** 

Segmentation (or isolation) of the CDE from the remainder of an entity’s network is not a PCI DSS requirement. However, it is strongly recommended as a method that may reduce the: 

- Scope of the PCI DSS assessment 

- Cost of the PCI DSS assessment 

- Cost and difficulty of implementing and maintaining PCI DSS controls 

- Risk to an organization relative to payment account data (reduced by consolidating that data into fewer, more controlled locations) 

Without adequate segmentation (sometimes called a "flat network"), the entire network is in scope for the PCI DSS assessment. Segmentation can be achieved using a number of physical or logical methods, such as properly configured internal network security controls, routers with strong access control lists, or other technologies that restrict access to a particular segment of a network. To be considered out of scope for PCI DSS, a system component must be properly segmented (isolated) from the CDE, such that the out-of-scope system component could not impact the security of cardholder data and/or sensitive authentication data, even if that component was compromised. 

An important prerequisite to reduce the scope of the CDE is a clear understanding of business needs and processes related to the storage, processing, and transmission of account data. Restricting account data to as few locations as possible by eliminating unnecessary data and consolidating necessary data may require reengineering of long-standing business practices. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 12_ 



Documenting account data flows via a data-flow diagram helps an entity fully understand how account data comes into an organization, where it resides within the organization, and how it traverses through various systems within the organization. Data-flow diagrams also illustrate all locations where account data is stored, processed, and transmitted. This information supports an entity implementing segmentation and can also support confirming that segmentation is being used to isolate the CDE from out-of-scope networks. 

If segmentation is used to reduce the scope of the PCI DSS assessment, the assessor must verify that the segmentation is adequate to reduce the scope of the assessment, as illustrated in Figure 2. At a high level, adequate segmentation isolates systems that store, process, or transmit account data from those that do not. However, the adequacy of a specific segmentation implementation is highly variable and depends on several factors such as a given network's configuration, the technologies deployed, and other controls that may be implemented. 

**Figure 2. Segmentation and Impact to PCI DSS Scope** 



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 13_ 



### **Wireless** 

If wireless technology is used to store, process, or transmit account data (for example, wireless point-of-sale devices), or if a wireless local area network (WLAN) is part of or connected to the CDE, the PCI DSS requirements and testing procedures for securing wireless environments apply and must be performed. 

Rogue wireless detection must be performed per PCI DSS Requirement 11.2.1 even when wireless is not used within the CDE and the entity has a policy that prohibits the use of wireless technology within its environment. This is because of the ease with which a wireless access point can be attached to a network, the difficulty in detecting its presence, and the increased risk presented by unauthorized wireless devices. 

Before wireless technology is implemented, an entity should carefully evaluate the need for the technology against the risk. Consider deploying wireless technology only for non-sensitive data transmission. 

### **When Cardholder Data and/or Sensitive Authentication Data is Accidentally Received via an Unintended Channel** 

There could be occurrences where an entity receives cardholder data and/or sensitive authentication data unsolicited via an insecure communication channel that was not intended for the purpose of receiving sensitive data. In this situation, the entity can choose to either: 

- Include the channel in the scope of their CDE and secure it according to PCI DSS 

- Or 

- Securely delete the data and implement measures to prevent the channel from being used in the future for sending such data. 

### **Encrypted Cardholder Data and Impact on PCI DSS Scope** 

Encryption of cardholder data with strong cryptography is an acceptable method of rendering the data unreadable according to PCI DSS Requirement 3.5. However, encryption alone is generally insufficient to render the cardholder data out of scope for PCI DSS and does not remove the need for PCI DSS in that environment. The entity’s environment is still in scope for PCI DSS due to the presence of cardholder data. For example, for a merchant card-present environment, there is physical access to the payment cards to complete a transaction and there may also be paper reports or receipts with cardholder data. Similarly, in merchant card-not-present environments, such as mailorder/telephone-order and e-commerce, payment card details are provided via channels that need to be evaluated and protected according to PCI DSS. 

The following are each in scope for PCI DSS: 

- Systems performing encryption and/or decryption of cardholder data, and systems performing key management functions, 

- Encrypted cardholder data that is not isolated from the encryption and decryption and key management processes, 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 14_ 



- Encrypted cardholder data that is present on a system or media that also contains the decryption key, 

- Encrypted cardholder data that is present in the same environment as the decryption key, 

- Encrypted cardholder data that is accessible to an entity that also has access to the decryption key. 

**_<mark>Note</mark>_** _<mark>: A PCI-listed P2PE solution can significantly reduce the number of PCI DSS requirements applicable to a merchant’s cardholder data environment. However, it does not completely remove the applicability of PCI DSS in the merchant environment.</mark>_ 

### **Encrypted Cardholder Data and Impact to PCI DSS Scope for Third-Party Service Providers** 

Where a third-party service provider (TPSP) receives and/or stores only data encrypted by another entity, and where they do not have the ability to decrypt the data, the TPSP may be able to consider the encrypted data out of scope if certain conditions are met. This is because responsibility for the data generally remains with the entity, or entities, with the ability to decrypt the data or impact the security of the encrypted data. Determining which party is responsible for specific PCI DSS controls will depend on several factors, including who has access to the decryption keys, the role performed by each party, and the agreement between parties. Responsibilities should be clearly defined and documented to ensure both the TPSP and the entity providing the encrypted data understand which entity is responsible for which security controls. 

As an example, a TPSP providing storage services receives and stores encrypted cardholder data provided by customers for back-up purposes. This TPSP does not have access to the encryption or decryption keys, nor does it perform any key management for its customers. The TPSP can exclude any such encrypted data when determining its PCI DSS scope. However, the TPSP does maintain responsibility for controlling access to the encrypted data storage as part of its service agreements with its customers. 

Responsibility for ensuring that the encrypted data and the cryptographic keys are protected according to applicable PCI DSS requirements is often shared between entities. In the above example, the customer determines which of their personnel are authorized to access the storage media, and the storage facility is responsible for managing the physical and/or logical access controls to ensure that only persons authorized by the customer are granted access to the storage media. The specific PCI DSS requirements applicable to a TPSP will depend on the services provided and the agreement between the two parties. In the example of a TPSP providing storage services, the physical and logical access controls provided by the TPSP will need to be reviewed at least annually. This review could be performed as part of the merchant’s PCI DSS assessment or, alternatively, the review could be performed, and controls validated, by the TPSP with appropriate evidence provided to the merchant. For information about “appropriate evidence,” see _Options for TPSPs to Validate PCI DSS Compliance for TPSP Services that Meet Customers’ PCI DSS Requirements._ 

As another example, a TPSP that receives only encrypted cardholder data for the purposes of routing to other entities, and that does not have access to the data or cryptographic keys, may not have any PCI DSS responsibility for that encrypted data. In this scenario, where the TPSP is not providing any security services or access controls, they may be considered the same as a public or untrusted network, and it would be the responsibility of the entity(s) sending/receiving account data through the TPSP’s network to ensure PCI DSS controls are applied to protect the data being transmitted. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 15_ 



### **Use of Third-Party Service Providers** 

An entity (referred to as the “customer” in this section) might choose to use a third-party service provider (TPSP) to store, process, or transmit account data or to manage in-scope system components on the customer’s behalf. Use of a TPSP may have an impact on the security of a customer’s CDE. 

**_<mark>Note</mark>_** _<mark>: Use of a PCI DSS compliant TPSP does not make a customer PCI DSS compliant, nor does it remove the customer’s responsibility for its own PCI DSS compliance. Even if a customer uses a TPSP, that customer remains responsible for confirming its own compliance as requested by organizations that manage compliance programs (for example, payment brands and acquirers). Customers should contact these organizations for any requirements.</mark>_ 

#### **_Using TPSPs and the Impact on Customers Meeting PCI DSS Requirement 12.8_** 

There are many different scenarios where a customer might use one or more TPSPs for functions within or related to the customer’s CDE. In all scenarios where a TPSP is used, the customer must manage and oversee all their TPSP relationships and monitor the PCI DSS compliance status of their TPSPs in accordance with Requirement 12.8, including TPSPs that: 

- Have access to the customer’s CDE, 

- Manage in-scope system components on the customer’s behalf, and/or 

- Can impact the security of the customer’s cardholder data and/or sensitive authentication data. 

Managing TPSP relationships in accordance with Requirement 12.8 includes performing due diligence, having appropriate agreements in place, identifying which requirements apply to the customer and which apply to the TPSP, and monitoring the compliance status of TPSPs at least annually. 

Requirement 12.8 does not specify that the customer’s TPSPs must be PCI DSS compliant, only that the customer monitors their compliance status as specified in the requirement. Therefore, a TPSP does not need to be PCI DSS compliant for its customer to meet Requirement 12.8. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 16_ 



#### **_Impact of Using TPSPs for Services that Meet Customers’ PCI DSS Requirements_** 

When the TPSP provides a service that meets a PCI DSS requirement(s) on the customer’s behalf or where that service may impact the security of the customer’s cardholder data and/or sensitive authentication data, then those requirements are in scope for the customer’s assessment and the compliance of that service will impact the customer’s PCI DSS compliance. The TPSP must demonstrate it meets applicable PCI DSS requirements for those requirements to be in place for its customers. For example, if an entity engages a TPSP to manage its network security controls, and the TPSP does not provide evidence that it meets the applicable requirements in PCI DSS Requirement 1, then those requirements are not in place for the customer’s assessment. As another example, TPSPs that store backups of cardholder data on behalf of customers would need to meet the applicable requirements related to access controls, physical security, etc., for their customers to consider those requirements in place for their assessments. 

#### **_Importance of Understanding Responsibilities Between TPSP Customers and TPSPs_** 

When a TPSP provides a service that meets a PCI DSS requirement(s) on the customer’s behalf or where that service may impact the security of the customer’s cardholder data and/or sensitive authentication data, it is important that customers and TPSPs clearly identify and understand the following: 

- The services and system components included in the scope of the TPSP’s PCI DSS assessment, 

- The specific PCI DSS requirements and sub-requirements covered by the TPSP’s PCI DSS assessment, 

- Any requirements that are the responsibility of the TPSP’s customers to include in their own PCI DSS assessments, and 

- Any PCI DSS requirements for which the responsibility is shared between the TPSP and its customers. 

For example, a cloud provider should clearly define which of its IP addresses are scanned as part of its quarterly vulnerability scan process and which IP addresses are their customers’ responsibility to scan. 

Per Requirement 12.9.2, TPSPs are required to support their customers’ requests for information about the TPSP’s PCI DSS compliance status related to the services provided to customers, and about which PCI DSS requirements are the responsibility of the TPSP, which are the responsibility of the customer, and any responsibilities shared between the customer and the TPSP. Refer to _Information Supplement: Third-Party Security Assurance_ for a sample responsibility matrix template that may be used for documenting and clarifying how responsibilities are shared between TPSPs and customers. 

_<mark>Note that not all TPSP relationships require that TPSPs provide customers with documentation of how responsibilities are shared between TPSPs and customers. TPSPs are only required to share such documentation if that TPSP is meeting a PCI DSS requirement(s) on the customer’s behalf, if responsibility for meeting a PCI DSS requirement is shared between the TPSP and its customer, or if the TPSP’s service may impact the security of the customer’s cardholder data and/or sensitive authentication data. While a TPSP may not be required to provide its customers with such documentation because there are no shared responsibilities, the TPSP still needs to support customers by providing their PCI DSS compliance status information, so that customers can manage and monitor their TPSPs in accordance with PCI DSS Requirement 12.8.</mark>_ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 17_ 



#### **_Options for TPSPs to Validate PCI DSS Compliance for TPSP Services that Meet Customers’ PCI DSS Requirements_** 

TPSPs are responsible for demonstrating their PCI DSS compliance as requested by organizations that manage compliance programs (for example, payment brands and acquirers). TPSPs should contact these organizations for any requirements. 

When a TPSP provides services that are intended to meet or facilitate meeting a customer’s PCI DSS requirements or that may impact the security of a customer’s cardholder data and/or sensitive authentication data, these requirements are in scope for the customer’s PCI DSS assessments. There are two options for TPSPs to validate compliance in this scenario: 

- **Annual assessment** : TPSP undergoes an annual PCI DSS assessment(s) and provides evidence to its customers to show the TPSP meets the applicable PCI DSS requirements; or 

- **Multiple, on-demand assessments** : If a TPSP does not undergo an annual PCI DSS assessment, it must undergo assessments upon request of their customers and/or participate in each of its customers’ PCI DSS assessments, with the results of each review provided to the respective customer(s). 

If the TPSP undergoes its own PCI DSS assessment, it is expected to provide sufficient evidence to its customers to verify that the scope of the TPSP’s PCI DSS assessment covered the services applicable to the customer, and that the relevant PCI DSS requirements were examined and determined to be in place. If the provider has an PCI DSS Attestation of Compliance (AOC), it is expected that the TPSP provides the AOC to customers upon request. The customer may also request relevant sections of the TPSP’s PCI DSS Report on Compliance (ROC). The ROC may be redacted to protect any confidential information. 

If the TPSP does not undergo its own PCI DSS assessment and therefore does not have an AOC, the TPSP is expected to provide specific evidence related to the applicable PCI DSS requirements, so that the customer (or its assessor) is able to confirm that the TPSP is meeting those PCI DSS requirements. 

#### **_TPSP’s Presence on a Payment Brand List(s) of PCI DSS Compliant Service Providers_** 

For a customer that is monitoring a TPSP’s compliance status in accordance with Requirement 12.8, the TPSP’s presence on a payment brand’s list of PCI DSS compliant service providers **_may be sufficient evidence_** of the TPSP’s compliance status if it is clear from the list that the services applicable to the customer were covered by the TPSP’s PCI DSS assessment. If it is not clear from the list, the customer should obtain other written confirmation that addresses the TPSP’s PCI DSS compliance status. 

For a customer that is looking for evidence of PCI DSS compliance for requirements that a TPSP meets on a customer’s behalf or where the service provided can impact the security of the customer’s cardholder data and/or sensitive authentication data, the TPSP’s presence on a payment brand’s list of PCI DSS compliant service providers **_is not sufficient evidence_** that the applicable PCI DSS requirements for that TPSP were included in the assessment. If the TPSP has an PCI DSS AOC, it is expected to provide it to customers upon request. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 18_ 



## **5 Best Practices for Implementing PCI DSS into Business-as-Usual Processes** 

An entity that implements business-as-usual processes, otherwise known as BAU, as part of their overall security strategy is taking measures to ensure that the security controls implemented to secure data and an environment continue to be implemented correctly and functioning properly as normal course of business. 

Some PCI DSS requirements are intended to act as BAU processes by monitoring security controls to ensure their effectiveness on an ongoing basis. This oversight by the entity assists with providing reasonable assurance that the compliance of its environment is preserved between PCI DSS assessments. While there are currently some BAU requirements defined within the standard, an entity should adopt additional BAU processes specific to their organization and environment when possible. BAU processes are a way to verify that automated and manual controls are performing as expected. Regardless of whether a PCI DSS requirement is automated or manual, it is important for BAU processes to detect anomalies, and alert and report so that responsible individuals address the situation in a timely manner. 

Examples of how PCI DSS should be incorporated into BAU activities include, but are not limited to: 

- Assigning overall responsibility and accountability for PCI DSS compliance to an individual or team. This can include a charter defined by executive management for a specific PCI DSS compliance program and communication to executive management. 

- Developing performance metrics to measure the effectiveness of security initiatives and continuous monitoring of security controls, including those that are heavily relied upon, such as network security controls, intrusion-detection systems/intrusion-prevention systems (IDS/IPS), change-detection mechanisms, anti-malware solutions, and access controls, to ensure they are operating effectively and as intended. 

- Reviewing logged data more frequently to gain insights to trends or behaviors that may not be obvious with only monitoring. 

- Ensuring that all failures in security controls are detected and responded to promptly. Processes to respond to security control failures should include: 

   - Restoring the security control. 

   - Identifying the cause of failure. 

   - Identifying and addressing any security issues that arose during the failure of the security control. 

   - Implementing mitigation, such as process or technical controls, to prevent the cause of the failure from recurring. 

   - Resuming monitoring of the security control, perhaps with enhanced monitoring for a period of time, to verify the control is operating effectively. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 19_ 



- Reviewing changes that could introduce security risks to the environment (for example, addition of new systems, changes in system or network configurations) prior to completing the change, and including the following: 

   - Perform a risk assessment to determine the potential impact to PCI DSS scope (for example, a new network security control rule that permits connectivity between a system in the CDE and another system could bring additional systems or networks into scope for PCI DSS). 

   - Identify PCI DSS requirements applicable to systems and networks affected by the changes (for example, if a new system is in scope for PCI DSS, it would need to be configured per system configuration standards, including change-detection mechanisms, anti-malware software, patches, and audit logging. These new systems and networks would need to be added to the inventory of inscope system components and to the quarterly vulnerability scan schedule). 

   - Update PCI DSS scope and implement security controls as appropriate. 

   - Update documentation to reflect implemented changes. 

- Reviewing the impact to PCI DSS scope and requirements upon changes to organizational structure (for example, a company merger or acquisition). 

- Reviewing external connections and third-party access periodically. 

- For entities that use third parties for software development, periodically confirming that those software development activities continue to comply with software development requirements in Requirement 6. 

- Performing periodic reviews to confirm that PCI DSS requirements continue to be in place and personnel follow established processes. Periodic reviews should cover all facilities and locations, including retail outlets and data centers, whether self-managed or if a TPSP is used. For example, periodic reviews can be used to confirm that configuration standards have been applied to applicable systems, default vendor accounts and passwords are removed or disabled, patches and anti-malware solutions are up to date, audit logs are being reviewed, and so on. The frequency of periodic reviews should be determined by the entity as appropriate for the size and complexity of their environment, if not otherwise stated in PCI DSS. 

These reviews can also be used to verify that required evidence for a PCI DSS assessment is being maintained. For example, evidence of audit logs, vulnerability scan reports, and reviews of network security control rulesets are necessary to assist the entity in preparing for its next PCI DSS assessment. 

- Establishing communication with all impacted parties, both external and internal, about newly identified threats and changes to the organization structure. Communication materials should help recipients understand the impact of threats, mitigating steps, and contact points for further information or escalation. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 20_ 



- Reviewing hardware and software technologies at least once every 12 months to confirm that they continue to be supported by the vendor and can meet the entity’s security requirements, including PCI DSS. If technologies are no longer supported by the vendor or cannot meet the entity’s security needs, the entity should prepare a remediation plan, including replacement of the technology, as necessary. 

**_<mark>Note</mark>_** _<mark>: Some best practices in this section are also included as PCI DSS requirements for certain entities. For example, those undergoing a full PCI DSS assessment, service providers validating to the additional “service provider only” requirements, and designated entities that are</mark> required to validate according to Appendix A3: Designated Entities Supplemental Validation._ 

_<mark>Each entity should consider implementing these best practices into their environment, even if the entity is not required to validate to them (for example, merchants undergoing self-assessment).</mark>_ 

Refer to _Best Practices for Maintaining PCI DSS Compliance_ in the Document Library on the PCI SSC website for additional guidance. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 21_ 



## **6 For Assessors: Sampling for PCI DSS Assessments** 

Sampling is an option for assessors conducting PCI DSS assessments to facilitate the assessment process when there are large numbers of items in a population being tested. 

While it is acceptable for an assessor to sample from similar items in a population being tested as part of its review of an entity’s PCI DSS compliance, it is not acceptable for an entity to apply PCI DSS requirements to only a sample of its environment (for example, requirements for quarterly vulnerability scans apply to all system components). Similarly, it is not acceptable for an assessor to review only a sample of PCI DSS requirements for compliance. 

While sampling allows assessors to test less than 100% of a given sampling population, assessors should always strive for the most complete review possible. Assessors are encouraged to use automated processes or other mechanisms if the complete population, regardless of size, can be tested quickly and efficiently with minimal impact on the resources of the entity being assessed. Where automated processes are not available to test 100% of a population, sampling is an equally acceptable approach. 

After considering the overall scope, complexity, and consistency of the environment being assessed, and the nature (automated or manual) of the processes used by an entity to meet a requirement, the assessor may independently select representative samples from the populations being reviewed in order to assess the entity’s compliance with PCI DSS requirements. Samples must be a representative selection of all variants of the population and must be sufficiently large to provide the assessor with assurance that controls are implemented as expected across the entire population. Where testing the periodic performance of a requirement (for example, weekly or quarterly, or periodically), the assessor should attempt to select a sample that represents the entire period covered by the assessment so that the assessor may make a reasonable judgment that the requirement was met throughout the assessment period. Testing the same sample of items year after year could allow unknown variations in the non-sampled items to remain undetected. Assessors must revalidate the sampling rationale for each assessment and consider previous sample sets. Different samples must be selected for each assessment. 

Appropriate selection of the sample depends on what is being considered in examining the sample members. For example, determining the presence of anti-malware on servers known to be affected by malicious software may lead to determining the population to be all servers in the environment, or all servers in the environment that are running a particular operating system, or all servers that are not mainframes, etc. Selection of an appropriate sample would then include representatives of ALL members of the identified population, including all servers running the identified operating system including all versions, as well as servers within the population that are used for different functions (for example, web servers, application servers, and database servers). 

In the case that a specific configuration item is being considered, the population might be appropriately divided, and separate sample groups identified. For example, a sample of all servers may not be appropriate when reviewing an operating system configuration setting, where different operating systems are present within the environment. In this case, samples from each operating system type would be appropriate in identifying that the configuration has been appropriately set for each operating system. Each sample set should include servers that are representative of each operating system type, including version, as well as representative functions. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 22_ 



Other examples of sampling include selections of personnel with similar or varied roles, based on the requirement being assessed, for example, a sample of administrators vs. a sample of all employees. 

The assessor is required to use professional judgment in the planning, performance, and evaluation of the sample to support their conclusion about whether and how the entity has met a requirement. The assessor’s goal in sampling is to obtain enough evidence to have a reasonable basis for their opinion. When independently selecting samples, assessors should consider the following: 

- The assessor must select the sample from the complete population without influence from the assessed entity. 

- If the entity has standardized processes and controls in place that ensure consistency and which is applied to each item in the population, the sample can be smaller than if the entity has no standardized processes/controls in place. The sample must be large enough to provide the assessor with reasonable assurance that items in the population adhere to the standardized processes that are applied to each item in the population. The assessor must verify that the standardized controls are implemented and working effectively. 

- If the entity has more than one type of standardized process in place (for example, for different types of business facilities/system components), the sample must include items subject to each type of process. For example, populations could be divided into subpopulations based on characteristics that may impact the consistency of the assessed requirements, such as the use of different processes or tools. Samples would then be selected from each sub-population. 

- If the entity has no standardized PCI DSS processes/controls in place and each item in the population is managed through nonstandardized processes, the sample must be larger for the assessor to be assured that the PCI DSS requirements are appropriately applied to each item in the population. 

- Samples of system components must include every type and combination being used. When an entity has more than one CDE, samples must include populations across all in-scope system components. For example, where applications are sampled, the sample must include all versions and platforms for each type of application. 

- Sample sizes must always be greater than one unless there is only one item in the given population, or an automated control is used where the assessor has confirmed the control is functioning as programmed for each assessed sample population. 

- If the assessor relies on standardized processes and controls being in place as a basis for selecting a sample, but then finds out during testing that standardized processes and controls are not in place or not operating effectively, the assessor should then increase the sample size to attempt to gain assurance that PCI DSS requirements are being met. 

For each instance where sampling is used, the assessor must: 

- Document the rationale behind the sampling technique and sample size. 

- Validate and document the standardized processes and controls used to determine sample size. 

- Explain how the sample is appropriate and representative of the overall population. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 23_ 



###### Figure 3 shows considerations for determining sample size. 

**Figure 3. PCI DSS Sampling Considerations** 



**_<mark>Note</mark>_** _<mark>: In PCI DSS v4.0, specific references to sampling have been removed from all testing procedures. These references were removed because calling out sampling only in some testing procedures may have implied that sampling was mandatory for those testing procedures (which it was not) or that sampling was only allowable where it was specifically mentioned. Assessors should select samples when it is appropriate to the population being tested, and, per above, render those decisions after considering the overall scope and complexity of an environment.</mark>_ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 24_ 



## **7 Description of Timeframes Used in PCI DSS Requirements** 

Certain PCI DSS requirements have been established with specific timeframes for activities that need to be performed consistently via a regularly scheduled and repeatable process. The intent is that the activity is performed at an interval as close to that timeframe as possible without exceeding it. The entity has the discretion to perform an activity more often than specified (for example, performing an activity monthly where the PCI DSS requirement specifies it be performed every three months). 

Table 4 outlines the frequency for the different time periods used in PCI DSS Requirements. 

**Table 4. PCI DSS Requirement Timeframes** 

|**Timeframes in PCI DSS**<br>**Requirements**|**Descriptions and Examples**|
|---|---|
|Daily|Every day of the year (not only on business days).|
|Weekly|At least once every seven days.|
|Monthly|At least once every 30 to 31 days, or on the n<sup>th</sup>day of the month.|
|Every three months<br>(“quarterly”)|At least once every 90 to 92 days, or on the n<sup>th</sup>day of each third month.|
|Every six months|At least once every 180 to 184 days, or on the n<sup>th</sup>day of each sixth month.|
|Every 12 months<br>(“annually”)|At least once every 365 (or 366 for leap years) days or on the same date every year.|
|Periodically|Frequency of occurrence is at the entity’s discretion and is documented and supported by the entity’s risk analysis. The entity<br>must demonstrate that the frequency is appropriate for the activity to be effective and to meet the intent of the requirement.|
|Immediately|Without delay. In real time or near real time.|
|Promptly|As soon as reasonably possible.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 25_ 



###### **Timeframes in PCI DSS Descriptions and Examples Requirements** 

Significant change There are several requirements that specify activities to be performed upon a significant change in an entity’s environment. While what constitutes a significant change is highly dependent on the configuration of a given environment, each of the following activities, at a minimum, has potential impacts on the security of the CDE and must be considered and evaluated to determine whether a change is a significant change for an entity in the context of related PCI DSS requirements: 

- New hardware, software, or networking equipment added to the CDE. 

- Any replacement or major upgrades of hardware and/or software in the CDE. 

- Any changes in the flow or storage of account data. 

- Any changes to the boundary of the CDE and/or to the scope of the PCI DSS assessment. 

- Any changes to the underlying supporting infrastructure of the CDE (including, but not limited to, changes to directory services, time servers, logging, and monitoring). 

- Any changes to third-party vendors/service providers (or services provided) that support the CDE or meet PCI DSS requirements on behalf of the entity. 

For other PCI DSS requirements, where the standard does not define a minimum frequency for recurring activities but instead allows for the requirement to be met “periodically,” the entity is expected to define the frequency as appropriate for its business. The frequency defined by the entity must be supported by the entity’s security policy and the risk analysis conducted according to PCI DSS Requirement 12.3.1. The entity must also be able to demonstrate that the frequency it has defined is appropriate for the activity to be effective and to meet the intent of the requirement. 

In both cases, where PCI DSS specifies a required frequency and where PCI DSS allows for “periodic” performance, the entity is expected to have documented and implemented processes to ensure that activities are performed within a reasonable timeframe, including at least the following: 

- The entity is promptly notified any time an activity is not performed per its defined schedule, 

- The entity determines the events that led to missing a scheduled activity, 

- The entity performs the activity as soon as possible after it is missed and either gets back on schedule or establishes a new schedule, 

- The entity produces documentation that shows the above elements occurred. 

When an entity has the above processes in place to detect and address when a scheduled activity is missed, a reasonable approach is allowable, meaning that if an activity is required to be performed at least once every three months, the entity is not automatically noncompliant if the activity is performed late where the entity’s documented and implemented process (per above) was followed. However, where no such process is in place and/or the activity was not performed according to schedule due to oversight, mismanagement, or lack of 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 26_ 



monitoring, the entity has not met the requirement. In such cases, the requirement will only be in place when the entity 1) documents (or reconfirms) the process per above to ensure the scheduled activity occurs on time, 2) re-establishes the schedule, and 3) provides evidence that the entity has performed the scheduled activity at least once per their schedule. 

**_Note_** _: Where an entity is being assessed for the first time against a PCI DSS requirement with a defined timeframe, it is considered an initial PCI DSS assessment for that requirement. This means the entity has never undergone a prior assessment to that requirement, where the assessment resulted in submission of a compliance validation document (for example, an AOC, SAQ, or ROC)._ 

_For an initial assessment against a requirement that has a defined timeframe, it is not required that the activity has been performed for every such timeframe during the previous year, if the assessor verifies:_ 

- _The activity was performed in accordance with the applicable requirement within the most recent timeframe (for example, the most recent three-month or six-month period), and_ 

- _The entity has documented policies and procedures for continuing to perform the activity within the defined timeframe._ 

_For subsequent years after the initial assessment, the activity must have been performed at least once within each required timeframe. For example, an activity required at least every three months must have been performed at least four times during the previous year at an interval that does not exceed 90-92 days._ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 27_ 



## **8 Approaches for Implementing and Validating PCI DSS** 

To support flexibility in how security objectives are met, there are two approaches for implementing and validating to PCI DSS. Entities should identify the approach best suited to their security implementation and use that approach to validate the controls. 

|**Defined**<br>**Approach**|Follows the traditional method for implementing and validating PCI DSS and uses the Requireme<br>defined within the standard. In the defined approach, the entity implements security controls to me<br>and the assessor follows the defined testing procedures to verify that requirements have been me<br>The defined approach supports entities with controls in place that meet PCI DSS requirements as<br>also suit entities that want more direction about how to meet security objectives, as well as entitie<br>or PCI DSS.<br>**Compensating Controls**<br>As part of the defined approach, entities that cannot meet a PCI DSS requirement explicitly as<br>stated due to a legitimate and documented technical or business constraint may implement<br>other, or_compensating, controls_, that sufficiently mitigate the risk associated with not meeting<br>the requirement. On an annual basis, any compensating controls must be documented by the<br>entity and reviewed and validated by the assessor and included with the Report on<br>Compliance submission.|nts and Testing Procedures<br>et the stated requirements,<br>t.<br>stated. This approach may<br>s new to information security<br>**_Note:_**_For more details,_<br>_seeAppendix B:_<br>_Compensating Controls_<br>_andAppendix C:_<br>_Compensating Controls_<br>_Worksheet. _|
|---|---|---|
|**Customized**<br>**Approach**|Focuses on the Objective of each PCI DSS requirement (if applicable), allowing entities to<br>implement controls to meet the requirement’s stated Customized Approach Objective in a way<br>that does not strictly follow the defined requirement. Because each customized<br>implementation will be different, there are no defined testing procedures; the assessor is<br>required to derive testing procedures that are appropriate to the specific implementation to<br>validate that the implemented controls meet the stated Objective.<br>The customized approach supports innovation in security practices, allowing entities greater<br>flexibility to show how their current security controls meet PCI DSS objectives. This approach<br>is intended for risk-mature entities that demonstrate a robust risk-management approach to secur<br>a dedicated risk-management department or an organization-wide risk management approach.<br>The controls implemented and validated using the customized approach are expected to meet or<br>by the requirement in the defined approach. The level of documentation and effort required to vali<br>implementations will also be greater than for the defined approach|ity, including, but not limited to,<br>exceed the security provided<br>date customized<br>**_Note:_**_For more details,_<br>_seeAppendix D:_<br>_Customized Approach and_<br>_PCI DSS v4.x: Sample_<br>_Templates to Support_<br>_Customized Approach_on<br>the PCI SSC website.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 28_ 



Most PCI DSS requirements can be met using either the defined or customized approach. However, several requirements do not have a stated Customized Approach Objective; the customized approach is not an option for these requirements. 

Entities can use both the defined and customized approaches within their environment. This means an entity could use the defined approach to meet some requirements and use the customized approach to meet other requirements. This also means that an entity could use the defined approach to meet a given PCI DSS requirement for one system component or within one environment and use the customized approach to meet that same PCI DSS requirement for a different system component or within a different environment. In this way, a PCI DSS assessment could include both defined and customized testing procedures. 

Figure 4 shows the two validation options for PCI DSS v4.x. 

**Figure 4. PCI DSS Validation Approaches** 



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 29_ 



## **9 Protecting Information About an Entity’s Security Posture** 

The processes related to becoming and maintaining a PCI DSS compliant environment results in many artifacts that an entity may consider sensitive and may want to protect as such, including such items as the following: 

- The Report on Compliance or Self-Assessment Questionnaire (the associated Attestation of Compliance is not considered sensitive and third-party service providers (TPSPs) are expected to share their AOC with customers). 

- Network diagrams and account data-flow diagrams, and security configurations and rules. 

- System configuration standards. 

- Cryptography and key management methods and protocols. 

Entities should review all the artifacts related to PCI DSS controls or the assessment and protect them in accordance with the entity’s security policies for this type of information. 

TPSPs are required (PCI DSS Requirement 12.9) to support their customers with the following: 

- Information needed for customers to monitor the TPSPs’ PCI DSS compliance status (to enable the customer to comply with Requirement 12.8), and 

- Evidence that the TPSP is meeting applicable PCI DSS requirements where the TPSP’s services are intended to meet or facilitate meeting a customer’s PCI DSS requirements, or where those services may impact the security of a customer’s cardholder data and/or sensitive authentication data. 

This section does not impact or negate a TPSP’s obligation to support and provide information to their customers per Requirement 12.9. 

For more details about expectations for TPSPs and relationships between TPSPs and customers, see _Use of Third-Party Service Providers_ . 

#### **_Protection of Confidential and Sensitive Information by Qualified Security Assessor Companies_** 

Each Qualified Security Assessor (QSA) Company signs an agreement with PCI SSC that they will adhere to the Qualification Requirements for QSAs. The _Protection of Confidential and Sensitive Information_ section of that document includes the following: 

“The QSA company must have and adhere to a documented process for protection of confidential and sensitive information. This must include adequate physical, electronic, and procedural safeguards consistent with industry-accepted practices to protect confidential and sensitive information against any threats or unauthorized access during storage, processing, and/or communicating of this information. 

“The QSA Company must maintain the privacy and confidentiality of information obtained in the course of performing its duties and obligations as a QSA Company, unless (and to the extent) disclosure is required by legal authority.” 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 30_ 



## **10 Testing Methods for PCI DSS Requirements** 

The testing methods identified in the Testing Procedures for each requirement describe the expected activities to be performed by the assessor to determine whether the entity has met the requirement. The intent behind each testing method is described as follows: 

- Examine: The assessor critically evaluates data evidence. Common examples include documents (electronic or physical), screenshots, configuration files, audit logs, and data files. 

- Observe: The assessor watches an action or views something in the environment. Examples of observation subjects include personnel performing a task or process, system components performing a function or responding to input, environmental conditions, and physical controls. 

- Interview: The assessor converses with individual personnel. Interview objectives may include confirmation of whether an activity is performed, descriptions of how an activity is performed, and whether personnel have particular knowledge or understanding. 

The testing methods are intended to allow the assessed entity to demonstrate how they have met a requirement. They also provide the assessed entity and the assessor with a common understanding of the assessment activities to be performed. The specific items to be examined or observed and personnel to be interviewed should be appropriate for both the requirement being assessed and each entity’s particular implementation. When documenting the assessment results, the assessor identifies the testing activities performed and the result of each activity. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 31_ 



## **11 Instructions and Content for Report on Compliance** 

Instructions and content for the Report on Compliance (ROC) are provided in the _PCI DSS Report on Compliance (ROC) Template_ . 

The PCI DSS Report on Compliance (ROC) Template must be used as the template for creating a PCI DSS Report on Compliance. 

Whether any entity is required to comply with or validate their compliance to PCI DSS is at the discretion of those organizations that manage compliance programs (such as payment brands and acquirers). Entities should contact these organizations to determine any reporting requirements and instructions. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 32_ 



## **12 PCI DSS Assessment Process** 

The PCI DSS assessment process includes the following high-level steps:<sup>5</sup> 

1. Confirm the scope of the PCI DSS assessment. 

2. Perform the PCI DSS assessment of the environment. 

3. Complete the applicable report for the assessment according to PCI DSS guidance and instructions. 

4. Complete the Attestation of Compliance for Service Providers or Merchants, as applicable, in its entirety. Official Attestations of Compliance are only available on the PCI SSC website. 

5. Submit the applicable PCI SSC documentation and the Attestation of Compliance, along with any other requested documentation— such as ASV scan reports—to the requesting organization (those that manage compliance programs such as payment brands and acquirers (for merchants), or other requesters (for service providers)). 

6. If required, perform remediation to address requirements that are not in place and provide an updated report. 

**_Note:_** _PCI DSS requirements are not considered to be in place if controls are not yet implemented or are scheduled to be completed at a future date. After any open or not-in-place items are addressed by the entity, the assessor will reassess to validate that the remediation is completed and that all requirements are satisfied. Refer to the following resources (available on the PCI SSC website) to document the PCI DSS assessment:_ 

- _For instructions about completing reports on compliance (ROC), refer to the PCI DSS Report on Compliance (ROC) Template._ 

- _For instructions about completing self-assessment questionnaires (SAQ), refer to the PCI DSS SAQ Instructions and Guidelines._ 

- _For instructions about submitting PCI DSS compliance validation reports, refer to the PCI DSS Attestation of Compliance._ 

> 5 The PCI DSS assessment process, and the roles and responsibilities for completion of each step, vary depending on the type of assessment and on compliance <u>programs, which are managed by payment brands and acquirers.</u> 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 33_ 



## **13 Additional References** 

Table 5 lists external organizations referenced within PCI DSS requirements or related guidance. These external organizations and their references are provided as information only and do not replace or extend any PCI DSS requirement. 

**Table 5. External Organizations Referenced in PCI DSS Requirements** 

|**Reference**|**Full Name**|
|---|---|
|ANSI|American National Standards Institute|
|CIS|Center for Internet Security|
|CSA|Cloud Security Alliance|
|ENISA|European Union Agency for Cybersecurity<br>(formerly European Network and Information Security Agency)|
|FIDO Alliance|The FIDO Alliance|
|ISO|International Organization for Standardization|
|NCSC|The UK National Cyber Security Centre|
|NIST|National Institute of Standards and Technology|
|OWASP|Open Web Application Security Project|
|SAFECode|Software Assurance Forum for Excellence in Code|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 34_ 



## **14 PCI DSS Versions** 

As of the published date of this document, PCI DSS v4.0.1 is the current version of the standard. 

Questions about the use of previous versions should be directed to those organizations that manage compliance programs (such as payment brands and acquirers). 

Table 6 summarizes PCI DSS versions and their relevant dates.<sup>6</sup> 

##### **Table 6. PCI DSS Versions** 

|**Version**|**Published**|**Retired**|
|---|---|---|
|PCI DSS v4.0.1 (this document)|June 2024|To be determined|
|PCI DSS v4.0|March 2022|31 December 2024|
|PCI DSS v3.2.1|May 2018|31 March 2024|
|PCI DSS 3.2|April 2016|31 December 2018|



6 Subject to change upon release of a new version of PCI DSS. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 35_ 



## **15 Detailed PCI DSS Requirements and Testing Procedures** 

Figure 5 describes the column headings and content for the PCI DSS requirements. 

**Figure 5. Understanding the Parts of the Requirements** 



<!-- Start of picture text -->
Figure 5. Understanding the Parts of the Requirements<br>Guidance  provides information<br>The  Requirement Description  at  to understand how to meet a<br>the X.X level organizes and  requirement. Guidance is not<br>describes the requirements that fall  required to be followed – it<br>under it.  does not replace or extend any<br>PCI DSS requirement.<br>Not every  Guidance  section<br>described here is present for<br>The  Defined Approach  each requirement.<br>Requirements and Testing  Not every section will be<br>Procedures  describes the  present for each requirement.<br>traditional method for<br>implementing and validating PCI<br>DSS using the Requirements and<br>Testing Procedures defined in the<br>standard.   Purpose  describes the goal,<br>benefit, or threat to be avoided;<br>why the requirement exists.<br>The  Customized Approach<br>Objective  is the intended goal or<br>outcome for the requirement. It  A  Good Practice  can be<br>must be met by entities using a  considered by the entity when<br>Customized Approach. Most PCI  meeting a requirement.<br>DSS requirements have this<br>Objective.<br>Appendix D describes<br>expectations for entities and  Definitions  Terms that may<br>assessors when the Customized  help understand the<br>Approach is used.   requirement.<br>Entities following the Defined<br>Approach can refer to the<br>Customized Approach<br>Objective  as guidance, but the  Applicability Notes  apply to both the Defined and  For each new PCI DSS v4.x  Examples  describe ways a<br>objective does not replace or  Customized Approach. It includes information that  requirement with an extended  requirement could be met.<br>supersede the Defined Approach  affects how the requirement is interpreted in the  implementation period.<br>Requirement.   context of the entity or in scoping.<br>These notes are an integral part of PCI DSS and<br>must be fully considered during an assessment.  Further Information  includes<br>references to relevant external<br>documentation.<br><!-- End of picture text -->

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 36_ 



#### **_Additional Requirements for Service Providers Only_** 

Some requirements apply only when the entity being assessed is a service provider. These are identified within the requirement as “ _Additional requirement for service providers only”_ and apply in addition to all other applicable requirements. Where the entity being assessed is both a merchant and a service provider, requirements noted as “ _Additional requirement for service providers only”_ apply to the service provider portion of the entity’s business. Requirements identified with “ _Additional requirement for service providers only”_ are also recommended as best practices for consideration by all entities. 

#### **_Appendices with Additional PCI DSS Requirements for Different Types of Entities_** 

In addition to the 12 principal requirements, PCI DSS Appendix A contains additional PCI DSS requirements for different types of entities. The sections within Appendix A include: 

- Appendix A1: Additional PCI DSS Requirements for Multi-Tenant Service Providers. 

- Appendix A2: Additional PCI DSS Requirements for Entities using SSL/Early TLS for Card-Present POS POI Terminal Connections. 

- Appendix A3: Designated Entities Supplemental Validation (DESV). 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 37_ 



### **Build and Maintain a Secure Network and Systems** 

#### **_Requirement 1: Install and Maintain Network Security Controls_** 

**Sections** 

- **1.1** Processes and mechanisms for installing and maintaining network security controls are defined and understood. 

- **1.2** Network security controls (NSCs) are configured and maintained. 

- **1.3** Network access to and from the cardholder data environment is restricted. 

- **1.4** Network connections between trusted and untrusted networks are controlled. 

- **1.5** Risks to the CDE from computing devices that are able to connect to both untrusted networks and the CDE are mitigated. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 38_ 



###### **Overview** 

Network security controls (NSCs), such as firewalls and other network security technologies, are network policy enforcement points that typically control network traffic between two or more logical or physical network segments (or subnets) based on pre-defined _policies_ or _rules_ . 

NSCs examine all network traffic entering (ingress) and leaving (egress) a segment and decide, based on the policies defined, whether the network traffic is allowed to pass or whether it should be rejected. Typically, NSCs are placed between environments with different security needs or levels of trust, however in some environments NSCs control the traffic to individual devices irrespective of trust boundaries. Policy enforcement generally occurs at layer 3 of the OSI model, but data present in higher layers is also frequently used to determine policy decisions. 

Traditionally this function has been provided by physical firewalls; however, now this functionality may be provided by virtual devices, cloud access controls, virtualization/container systems, and other software-defined networking technology. 

NSCs are used to control traffic within an entity’s own networks—for example, between highly sensitive and less sensitive areas—and also to protect the entity’s resources from exposure to untrusted networks. The cardholder data environment (CDE) is an example of a more sensitive area within an entity’s network. Often, seemingly insignificant paths to and from untrusted networks can provide unprotected pathways into sensitive systems. NSCs provide a key protection mechanism for any computer network. 

Common examples of untrusted networks include the Internet, dedicated connections such as business-to-business communication channels, wireless networks, carrier networks (such as cellular), third-party networks, and other sources outside the entity’s ability to control. Furthermore, untrusted networks also include corporate networks that are considered out-of-scope for PCI DSS, because they are not assessed, and therefore must be treated as untrusted because the existence of security controls has not been verified. While an entity may consider an internal network to be trusted from an infrastructure perspective, if a network is out of scope for PCI DSS, that network must be considered untrusted for PCI DSS. 

Refer to _Appendix G_ for definitions of PCI DSS terms. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 39_ 



###### **Requirements and Testing Procedures Guidance** 

###### **1.1 Processes and mechanisms for installing and maintaining network security controls are defined and understood.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**1.1.1**All security policies and operational<br>procedures that are identified in Requirement 1 are:<br>•<br>Documented.<br>•<br>Kept up to date.<br>•<br>In use.<br>•<br>Known to all affected parties.|**1.**1.1 Examine documentation and interview<br>personnel to verify that security policies and<br>operational procedures identified in Requirement 1<br>are managed in accordance with all elements<br>specified in this requirement.|Requirement 1.1.1 is about effectively managing<br>and maintaining the various policies and<br>procedures specified throughout Requirement 1.<br>While it is important to define the specific policies<br>or procedures called out in Requirement 1, it is<br>equally important to ensure they are properly<br>documented, maintained, and disseminated.<br>**Good Practice**|
|**Customized Approach Objective**||It is important to update policies and procedures<br>as needed to address changes in processes,|
|Expectations, controls, and oversight for meeting<br>activities within Requirement 1 are defined,<br>understood, and adhered to by affected personnel.<br>All supporting activities are repeatable, consistently<br>applied, and conform to management’s intent.||technologies, and business objectives. For these<br>reasons, consider updating these documents as<br>soon as possible after a change occurs and not<br>only on a periodic cycle.<br>**Definitions**<br>Security policies define the entity’s security<br>objectives and principles. Operational procedures<br>describe how to perform activities, and define the<br>controls, methods, and processes that are<br>followed to achieve the desired result in a<br>consistent manner and in accordance with policy<br>objectives.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 40_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**1.1.2**Roles and responsibilities for performing<br>activities in Requirement 1 are documented,<br>assigned, and understood.|**1.1.2.a**Examine documentation to verify that<br>descriptions of roles and responsibilities for<br>performing activities in Requirement 1 are<br>documented and assigned.|If roles and responsibilities are not formally<br>assigned, personnel may not be aware of their<br>day-to-day responsibilities and critical activities<br>may not occur.<br>**Good Practice**|
||**1.1.2.b**Interview personnel responsible for<br>performing activities in Requirement 1 to verify that<br>roles and responsibilities are assigned as<br>documented and are understood.|Roles and responsibilities may be documented<br>within policies and procedures or maintained<br>within separate documents.<br>As part of communicating roles and<br>responsibilities, entities can consider having<br>personnel acknowledge their acceptance and|
|**Customized Approach Objective**||understanding of their assigned roles and<br>responsibilities.|
|Day-to-day responsibilities for performing all the<br>activities in Requirement 1 are allocated. Personnel<br>are accountable for successful, continuous<br>operation of these requirements.||**Examples**<br>A method to document roles and responsibilities<br>is a responsibility assignment matrix that includes<br>who is responsible, accountable, consulted, and<br>informed (also called a RACI matrix).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 41_ 



###### **Requirements and Testing Procedures Guidance** 

###### **1.2 Network security controls (NSCs) are configured and maintained.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**1.2.1**Configuration standards for NSC rulesets are:<br>•<br>Defined.<br>•<br>Implemented.<br>•<br>Maintained.|**1.2.1.a**Examine the configuration standards for<br>NSC rulesets to verify the standards are in<br>accordance with all elements specified in this<br>requirement.|The implementation of these configuration<br>standards results in the NSC being configured<br>and managed to properly perform their security<br>function (often referred to as the ruleset).<br>**Good Practice**|
||**1.2.1.b**Examine configuration settings for NSC<br>rulesets to verify that rulesets are implemented|These standards often define the requirements for<br>acceptable protocols, ports that are permitted to|
|**Customized Approach Objective**|<br>according to the configuration standards.|be used, and specific configuration requirements<br>that are acceptable. Configuration standards may|
|The way that NSCs are configured and operate are<br>defined and consistently applied.||also outline what the entity considers not<br>acceptable or not permitted within its network.<br>**Definitions**|
|||NSCs are key components of a network<br>architecture. Most commonly, NSCs are used at<br>the boundaries of the CDE to control network<br>traffic flowing inbound and outbound from the<br>CDE.|
|||Configuration standards outline an entity’s<br>minimum requirements for the configuration of its<br>NSCs.<br>**Examples**<br>Examples of NSCs covered by these<br>configuration standards include, but are not<br>limited to, firewalls, routers configured with<br>access control lists, and cloud virtual networks.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 42_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**1.2.2**All changes to network connections and to<br>configurations of NSCs are approved and managed<br>in accordance with the change control process<br>defined at Requirement 6.5.1.|**1.2.2.a**Examine documented procedures to verify<br>that changes to network connections and<br>configurations of NSCs are included in the formal<br>change control process in accordance with<br>Requirement 6.5.1.|Following a structured change control process for<br>all changes to NSCs reduces the risk that a<br>change could introduce a security vulnerability.<br>**Good Practice**<br>Changes should be approved by individuals with<br>the appropriate authority and knowledge to|
||**1.2.2.b**Examine network configuration settings to<br>identify changes made to network connections.<br>Interview responsible personnel and examine<br>change control records to verify that identified<br>changes to network connections were approved<br>and managed in accordance with Requirement<br>6.5.1.|understand the impact of the change. Verification<br>should provide reasonable assurance that the<br>change did not adversely impact the security of<br>the network and that the change performs as<br>expected.<br>To avoid having to address security issues<br>introduced by a change, all changes should be<br>approved prior to being implemented and verified|
||**1.2.2.c**Examine network configuration settings to<br>identify changes made to configurations of NSCs.|after the change is implemented. Once approved<br>and verified, network documentation should be|
|**Customized Approach Objective**|<br>Interview responsible personnel and examine<br>change control records to verify that identified|updated to include the changes to prevent<br>inconsistencies between network documentation|
|Changes to network connections and NSCs cannot<br>result in misconfiguration, implementation of<br>insecure services, or unauthorized network<br>connections.|<br>changes to configurations of NSCs were approved<br>and managed in accordance with Requirement<br>6.5.1.|and the actual configuration.|
|**Applicability Notes**|||
|Changes to network connections include the<br>addition, removal, or modification of a connection.<br>Changes to NSC configurations include those<br>related to the component itself as well as those<br>affecting how it performs its security function.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 43_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**1.2.3**An accurate network diagram(s) is maintained<br>that shows all connections between the CDE and<br>other networks, including any wireless networks.<br>**Customized Approach Objective**|**1.2.3.a**Examine diagram(s) and network<br>configurations to verify that an accurate network<br>diagram(s) exists in accordance with all elements<br>specified in this requirement.|Maintaining an accurate and up-to-date network<br>diagram(s) prevents network connections and<br>devices from being overlooked and unknowingly<br>left unsecured and vulnerable to compromise.<br>A properly maintained network diagram(s) helps<br>an organization verify its PCI DSS scope by<br>identifying systems connecting to and from the<br>CDE.|
|A representation of the boundaries between the<br>CDE, all trusted networks, and all untrusted<br>networks, is maintained and available.|**1.2.3.b**Examine documentation and interview<br>responsible personnel to verify that the network<br>diagram(s) is accurate and updated when there are<br>changes to the environment.|**Good Practice**<br>All connections to and from the CDE should be<br>identified, including systems providing security,<br>management, or maintenance services to CDE|
|**Applicability Notes**||system components. Entities should consider<br>including the following in their network diagrams:|
|A current network diagram(s) or other technical or<br>topological solution that identifies network<br>connections and devices can be used to meet this<br>requirement.||•<br>All locations, including retail locations, data<br>centers, corporate locations, cloud providers,<br>etc.<br>•<br>Clear labeling of all network segments.<br>•<br>All security controls providing segmentation,<br>including unique identifiers for each control<br>(for example, name of control, make, model,<br>and version).<br>•<br>All in-scope system components, including<br>NSCs, web app firewalls, anti-malware<br>solutions, change management solutions,<br>IDS/IPS, log aggregation systems, payment<br>terminals, payment applications, HSMs, etc.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 44_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**1.2.3**_(continued)_||•<br>Clear labeling of any out-of-scope areas on<br>the diagram via a shaded box or other<br>mechanism.<br>•<br>Date of last update, and names of people that<br>made and approved the updates.<br>•<br>A legend or key to explain the diagram.<br>Diagrams should be updated by authorized<br>personnel to ensure diagrams continue to provide<br>an accurate description of the network.|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**1.2.4**An accurate data-flow diagram(s) is<br>maintained that meets the following:<br>•<br>Shows all account data flows across systems<br>and networks.|**1.2.4.a**Examine data-flow diagram(s) and<br>interview personnel to verify the diagram(s) show<br>all account data flows in accordance with all<br>elements specified in this requirement.|An up-to-date, readily available data-flow diagram<br>helps an organization understand and keep track<br>of the scope of its environment by showing how<br>account data flows across networks and between<br>individual systems and devices.|
|•<br>Updated as needed upon changes to the<br>environment.|**1.2.4.b**Examine documentation and interview<br>responsible personnel to verify that the data-flow|Maintaining an up-to-date data-flow diagram(s)<br>prevents account data from being overlooked and<br>|
|**Customized Approach Objective**|diagram(s) is accurate and updated when there are<br>changes to the environment.|unknowingly left unsecured.<br>**Good Practice**|
|A representation of all transmissions of account<br>data between system components and across<br>network segments is maintained and available.||The data-flow diagram should include all<br>connection points where account data is received<br>into and sent out of the network, including<br>connections to open, public networks, application|
|**Applicability Notes**||processing flows, storage, transmissions between<br>systems and networks, and file backups.|
|A data-flow diagram(s) or other technical or|||
|topological solution that identifies flows of account<br>data across systems and networks can be used to<br>meet this requirement.||_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 45_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**1.2.4**_(continued)_|The data-flow diagram is meant to be in addition<br>to the network diagram and should reconcile with<br>and augment the network diagram. As a best<br>practice, entities can consider including the<br>following in their data-flow diagrams:<br>•<br>All processing flows of account data, including<br>authorization, capture, settlement,<br>chargeback, and refunds.<br>•<br>All distinct acceptance channels, including<br>card-present, card-not-present, and e-<br>commerce.<br>•<br>All types of data receipt or transmission,<br>including any involving hard copy/paper<br>media.<br>•<br>The flow of account data from the point where<br>it enters the environment, to its final<br>disposition.<br>•<br>Where account data is transmitted and<br>processed, where it is stored, and whether<br>storage is short term or long term.<br>•<br>The source of all account data received (for<br>example, customers, third party, etc.), and any<br>entities with which account data is shared.<br>•<br>Date of last update, and names of people that<br>made and approved the updates.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 46_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**1.2.5**All services, protocols, and ports allowed are<br>identified, approved, and have a defined business<br>need.<br>**Customized Approach Objective**<br>Unauthorized network traffic (services, protocols, or<br>packets destined for specific ports) cannot enter or<br>leave the network.|**1.2.5.a**Examine documentation to verify that a list<br>exists of all allowed services, protocols, and ports,<br>including business justification and approval for<br>each.<br>**1.2.5.b**Examine configuration settings for NSCs to<br>verify that only approved services, protocols, and<br>ports are in use.|Compromises often happen due to unused or<br>insecure services (for example, telnet and FTP),<br>protocols, and ports, since these can lead to<br>unnecessary points of access being opened into<br>the CDE. Additionally, services, protocols, and<br>ports that are enabled but not in use are often<br>overlooked and left unsecured and unpatched. By<br>identifying the services, protocols, and ports<br>necessary for business, entities can ensure that<br>all other services, protocols, and ports are<br>disabled or removed.<br>**Good Practice**<br>The security risk associated with each service,<br>protocol, and port allowed should be understood.<br>Approvals should be granted by personnel<br>independent of those managing the configuration.<br>Approving personnel should possess knowledge<br>and accountability appropriate for making<br>approval decisions.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 47_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**1.2.6**Security features are defined and<br>implemented for all services, protocols, and ports<br>that are in use and considered to be insecure, such<br>that the risk is mitigated.|**1.2.6.a**Examine documentation that identifies all<br>insecure services, protocols, and ports in use to<br>verify that for each, security features are defined to<br>mitigate the risk.|Compromises take advantage of insecure<br>network configurations.<br>**Good Practice**<br>If insecure services, protocols, or ports are<br>necessary for business, the risk posed by these|
||**1.2.6.b**Examine configuration settings for NSCs to<br>verify that the defined security features are<br>implemented for each identified insecure service,<br>protocol, and port.|services, protocols, and ports should be clearly<br>understood and accepted by the organization, the<br>use of the service, protocol, or port should be<br>justified, and the security features that mitigate<br>the risk of using these services, protocols, and<br>ports should be defined and implemented by the|
|**Customized Approach Objective**||entity.<br>**Further Information**|
|The specific risks associated with the use of<br>insecure services, protocols, and ports are<br>understood, assessed, and appropriately mitigated.||For guidance on services, protocols, or ports<br>considered to be insecure, refer to industry<br>standards and guidance (for example, from NIST,<br>ENISA, OWASP).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 48_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**1.2.7**Configurations of NSCs are reviewed at least<br>once every six months to confirm they are relevant<br>and effective.|**1.2.7.a**Examine documentation to verify<br>procedures are defined for reviewing<br>configurations of NSCs at least once every six<br>months.|Such a review gives the organization an<br>opportunity to clean up any unneeded, outdated,<br>or incorrect rules and configurations which could<br>be utilized by an unauthorized person.<br>Furthermore, it ensures that all rules and|
||**1.2.7.b**Examine documentation of reviews of<br>configurations for NSCs and interview responsible<br>personnel to verify that reviews occur at least once<br>every six months.|configurations allow only authorized services,<br>protocols, and ports that match the documented<br>business justifications.<br>**Good Practice**<br>This review, which can be implemented using|
||**1.2.7.c**Examine configurations for NSCs to verify<br>that configurations identified as no longer being|manual, automated, or system-based methods, is<br>intended to confirm that the settings that manage<br>|
|**Customized Approach Objective**|<br>supported by a business justification are removed<br>or updated.|traffic rules, what is allowed in and out of the<br>network, match the approved configurations.|
|NSC configurations that allow or restrict access to||The review should provide confirmation that all|
|trusted networks are verified periodically to ensure<br>that only authorized connections with a current<br>business justification are permitted.||permitted access has a justified business reason.<br>Any discrepancies or uncertainties about a rule or<br>configuration should be escalated for resolution.<br>While this requirement specifies that this review<br>occur at least once every six months,<br>organizations with a high volume of changes to<br>their network configurations may wish to consider<br>performing reviews more frequently to ensure that<br>the configurations continue to meet the needs of<br>the business.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 49_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**1.2.8**Configuration files for NSCs are:<br>•<br>Secured from unauthorized access.<br>•<br>Kept consistent with active network<br>configurations.|**1.2.8**Examine configuration files for NSCs to verify<br>they are in accordance with all elements specified<br>in this requirement.|To prevent unauthorized configurations from<br>being applied to the network, stored files with<br>configurations for network controls need to be<br>kept up to date and secured against unauthorized<br>changes.<br>Keeping configuration information current and|
|**Customized Approach Objective**||secure ensures that the correct settings for NSCs<br>are applied whenever the configuration is run.|
|NSCs cannot be defined or modified using untrusted<br>configuration objects (including files).||**Examples**<br>If the secure configuration for a router is stored in|
|**Applicability Notes**||non-volatile memory, when that router is restarted<br>or rebooted, these controls should ensure that its|
|Any file or setting used to configure or synchronize<br>NSCs is considered to be a “configuration file.” This<br>includes files, automated and system-based<br>controls, scripts, settings, infrastructure as code, or<br>other parameters that are backed up, archived, or<br>stored remotely.||secure configuration is reinstated.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 50_ 



###### **Requirements and Testing Procedures Guidance** 

|**1.3 Network access to and from the cardhold**|**er data environment is restricted.**||
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**1.3.1**Inbound traffic to the CDE is restricted as<br>follows:<br>•<br>To only traffic that is necessary.<br>•<br>All other traffic is specifically denied.|**1.3.1.a**Examine configuration standards for NSCs<br>to verify that they define restricting inbound traffic<br>to the CDE is in accordance with all elements<br>specified in this requirement.|This requirement aims to prevent malicious<br>individuals from accessing the entity’s network via<br>unauthorized IP addresses or from using<br>services, protocols, or ports in an unauthorized<br>manner.|
||**1.3.1.b**Examine configurations of NSCs to verify<br>that inbound traffic to the CDE is restricted in|**Good Practice**<br>All traffic inbound to the CDE, regardless of where|
|**Customized Approach Objective**<br>Unauthorized traffic cannot enter the CDE.|<br>accordance with all elements specified in this<br>requirement.|it originates, should be evaluated to ensure it<br>follows established, authorized rules. Connections<br>should be inspected to ensure traffic is restricted<br>to only authorized communications—for example,<br>by restricting source/destination addresses and<br>ports, and blocking of content.<br>**Examples**<br>Implementing a rule that denies all inbound and<br>outbound traffic that is not specifically needed—<br>for example, by using an explicit “deny all” or<br>implicit deny after allow statement—helps to<br>prevent inadvertent holes that would allow<br>unintended and potentially harmful traffic.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 51_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**1.3.2**Outbound traffic from the CDE is restricted as<br>follows:<br>•<br>To only traffic that is necessary.<br>•<br>All other traffic is specifically denied.|**1.3.2.a**Examine configuration standards for NSCs<br>to verify that they define restricting outbound traffic<br>from the CDE in accordance with all elements<br>specified in this requirement.|This requirement aims to prevent malicious<br>individuals and compromised system components<br>within the entity’s network from communicating<br>with an untrusted external host.<br>**Good Practice**|
||**1.3.2.b**Examine configurations of NSCs to verify<br>that outbound traffic from the CDE is restricted in|All traffic outbound from the CDE, regardless of<br>the destination, should be evaluated to ensure it|
|**Customized Approach Objective**<br>Unauthorized traffic cannot leave the CDE.|accordance with all elements specified in this<br>requirement.|follows established, authorized rules. Connections<br>should be inspected to restrict traffic to only<br>authorized communications—for example, by<br>restricting source/destination addresses and<br>ports, and blocking of content.<br>**Examples**<br>Implementing a rule that denies all inbound and<br>outbound traffic that is not specifically needed—<br>for example, by using an explicit “deny all” or<br>implicit deny after allow statement—helps to<br>prevent inadvertent holes that would allow<br>unintended and potentially harmful traffic.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 52_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**1.3.3**NSCs are installed between all wireless<br>networks and the CDE, regardless of whether the<br>wireless network is a CDE, such that:<br>•<br>All wireless traffic from wireless networks into<br>the CDE is denied by default.|**1.3.3**Examine configuration settings and network<br>diagrams to verify that NSCs are implemented<br>between all wireless networks and the CDE, in<br>accordance with all elements specified in this<br>requirement.|The known (or unknown) implementation and<br>exploitation of wireless technology within a<br>network is a common path for malicious<br>individuals to gain access to the network and<br>account data. If a wireless device or network is<br>installed without the entity’s knowledge, a|
|•<br>Only wireless traffic with an authorized business<br>purpose is allowed into the CDE.||malicious individual could easily and “invisibly”<br>enter the network. If NSCs do not restrict access<br>from wireless networks into the CDE, malicious|
|**Customized Approach Objective**||individuals that gain unauthorized access to the<br>wireless network can easily connect to the CDE|
|Unauthorized traffic cannot traverse network<br>boundaries between any wireless networks and<br>wired environments in the CDE.||and compromise account information.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 53_ 



###### **Requirements and Testing Procedures Guidance** 

###### **1.4 Network connections between trusted and untrusted networks are controlled.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**1.4.1**NSCs are implemented between trusted and<br>untrusted networks.|**1.4.1.a**Examine configuration standards and<br>network diagrams to verify that NSCs are defined<br>between trusted and untrusted networks.|Implementing NSCs at every connection coming<br>into and out of trusted networks allows the entity<br>to monitor and control access and minimizes the<br>chances of a malicious individual obtaining<br>access to the internal network via an unprotected|
|**Customized Approach Objective**<br>Unauthorized traffic cannot traverse network<br>boundaries between trusted and untrusted<br>networks.|**1.4.1.b**Examine network configurations to verify<br>that NSCs are in place between trusted and<br>untrusted networks, in accordance with the<br>documented configuration standards and network<br>diagrams.|connection.<br>**Examples**<br>An entity could implement a DMZ, which is a part<br>of the network that manages connections<br>between an untrusted network (for examples of<br>untrusted networks refer to the Requirement 1<br>Overview) and services that an organization<br>needs to have available to the public, such as a<br>web server. Please note that if an entity’s DMZ<br>processes or transmits account data (for example,<br>e-commerce website), it is also considered a<br>CDE.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 54_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

**Defined Approach Requirements Defined Approach Testing Procedures Purpose** Ensuring that public access to a system **1.4.2** Inbound traffic from untrusted networks to **1.4.2** Examine vendor documentation and component is specifically authorized reduces the trusted networks is restricted to: configurations of NSCs to verify that inbound traffic risk of system components being unnecessarily • Communications with system components that from untrusted networks to trusted networks is exposed to untrusted networks. restricted in accordance with all elements specified are authorized to provide publicly accessible services, protocols, and ports. in this requirement. **Good Practice** • Stateful responses to communications initiated System components that provide publicly accessible services, such as email, web, and by system components in a trusted network. DNS servers, are the most vulnerable to threats • All other traffic is denied. originating from untrusted networks. Ideally, such systems are placed within a **Customized Approach Objective** dedicated trusted network that is public facing (for example, a DMZ) but that is separated via NSCs Only traffic that is authorized or that is a response to from more sensitive internal systems, which helps a system component in the trusted network can protect the rest of the network in the event these enter a trusted network from an untrusted network. externally accessible systems are compromised. This functionality is intended to prevent malicious **Applicability Notes** actors from accessing the organization's internal network from the Internet, or from using services, The intent of this requirement is to address protocols, or ports in an unauthorized manner. communication sessions between trusted and untrusted networks, rather than the specifics of Where this functionality is provided as a built-in protocols. feature of an NSC, the entity should ensure that its configurations do not result in the functionality This requirement does not limit the use of UDP or being disabled or bypassed. 

This requirement does not limit the use of UDP or other connectionless network protocols if state is maintained by the NSC. 

###### **Definitions** 

Maintaining the "state" (or status) for each connection into a network means the NSC “knows” whether an apparent response to a previous connection is a valid, authorized response (since the NSC retains each connection’s status) or whether it is malicious traffic trying to fool the NSC into allowing the connection. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 55_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**1.4.3**Anti-spoofing measures are implemented to<br>detect and block forged source IP addresses from<br>entering the trusted network.|**1.4.3**Examine vendor documentation and<br>configurations for NSCs to verify that anti-spoofing<br>measures are implemented to detect and block<br>|Filtering packets coming into the trusted network<br>helps to, among other things, ensure packets are<br>not “spoofed” to appear as if they are coming from<br>an organization’s own internal network. For|
|**Customized Approach Objective**<br>Packets with forged IP source addresses cannot<br>enter a trusted network.|forged source IP addresses from entering the<br>trusted network.|example, anti-spoofing measures prevent internal<br>addresses originating from the Internet from<br>passing into the DMZ.<br>**Good Practice**<br>Products usually come with anti-spoofing set as a<br>default and may not be configurable. Entities<br>should consult the vendor's documentation for<br>more information.|
|||**Examples**|
|||Normally, a packet contains the IP address of the<br>computer that originally sent it so other computers<br>in the network know where the packet originated.<br>Malicious individuals will often try to spoof (or<br>imitate) the sending IP address to fool the target<br>system into believing the packet is from a trusted<br>source.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 56_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**1.4.4**System components that store cardholder<br>data are not directly accessible from untrusted<br>networks.|**1.4.4.a**Examine the data-flow diagram and<br>network diagram to verify that it is documented that<br>system components storing cardholder data are<br>not directly accessible from the untrusted<br>networks.|Cardholder data that is directly accessible from an<br>untrusted network, for example, because it is<br>stored on a system within the DMZ or in a cloud<br>database service, is easier for an external<br>attacker to access because there are fewer<br>defensive layers to penetrate. Using NSCs to<br>ensure that system components that store|
|**Customized Approach Objective**|**1.4.4.b**Examine configurations of NSCs to verify<br>that controls are implemented such that system<br>components storing cardholder data are not<br>directly accessible from untrusted networks.|cardholder data (such as a database or a file) can<br>only be directly accessed from trusted networks<br>can prevent unauthorized network traffic from<br>reaching the system component.|
|Stored cardholder data cannot be accessed from<br>untrusted networks.|||
|**Applicability Notes**|||
|This requirement is not intended to apply to storage<br>of account data in volatile memory but does apply<br>where memory is being treated as persistent<br>storage (for example, RAM disk). Account data can<br>only be stored in volatile memory during the time<br>necessary to support the associated business<br>process (for example, until completion of the related<br>payment card transaction).|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 57_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**1.4.5**The disclosure of internal IP addresses and<br>routing information is limited to only authorized<br>parties.|**1.4.5.a**Examine configurations of NSCs to verify<br>that the disclosure of internal IP addresses and<br>routing information is limited to only authorized<br>parties.|Restricting the disclosure of internal, private, and<br>local IP addresses is useful to prevent a hacker<br>from obtaining knowledge of these IP addresses<br>and using that information to access the network.<br>**Good Practice**|
||**1.4.5.b**Interview personnel and examine<br>documentation to verify that controls are|Methods used to meet the intent of this<br>requirement may vary, depending on the specific<br>|
|**Customized Approach Objective**<br>Internal network information is protected from<br>unauthorized disclosure.|implemented such that any disclosure of internal IP<br>addresses and routing information is limited to only<br>authorized parties.|networking technology being used. For example,<br>the controls used to meet this requirement may<br>be different for IPv4 networks than for IPv6<br>networks.<br>**Examples**<br>Methods to obscure IP addressing may include,<br>but are not limited to:<br>•<br>IPv4 Network Address Translation (NAT).<br>•<br>Placing system components behind proxy<br>servers/NSCs.<br>•<br>Removal or filtering of route advertisements<br>for internal networks that use registered<br>addressing.<br>•<br>Internal use of RFC 1918 (IPv4) or use IPv6<br>privacy extension (RFC 4941) when initiating<br>outgoing sessions to the internet.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 58_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **1.5 Risks to the CDE from computing devices that are able to connect to both untrusted networks and the CDE are mitigated.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**1.5.1**Security controls are implemented on any<br>computing devices, including company- and<br>employee-owned devices, that connect to both<br>untrusted networks (including the Internet) and the<br>CDE as follows:<br>•<br>Specific configuration settings are defined to<br>|**1.5.1.a**Examine policies and configuration<br>standards and interview personnel to verify<br>security controls for computing devices that<br>connect to both untrusted networks, and the CDE,<br>are implemented in accordance with all elements<br>specified in this requirement.|Computing devices that are allowed to connect to<br>the Internet from outside the corporate<br>environment—for example, desktops, laptops,<br>tablets, smartphones, and other mobile computing<br>devices used by employees—are more vulnerable<br>to Internet-based threats.<br>Use of security controls such as host-based|
|prevent threats being introduced into the<br>entity’s network.<br>•<br>Security controls are actively running.<br>•<br>Security controls are not alterable by users of<br>the computing devices unless specifically<br>documented and authorized by management on<br>a case-by-case basis for a limited period.|**1.5.1.b**Examine configuration settings on<br>computing devices that connect to both untrusted<br>networks and the CDE to verify settings are<br>implemented in accordance with all elements<br>specified in this requirement.|controls (for example, personal firewall software<br>or end-point protection solutions), network-based<br>security controls (for example, firewalls, network-<br>based heuristics inspection, and malware<br>simulation), or hardware, helps to protect devices<br>from Internet-based attacks, which could use the<br>device to gain access to the organization’s<br>systems and data when the device reconnects to<br>the network.|
|**Customized Approach Objective**<br>Devices that connect to untrusted environments and<br>also connect to the CDE cannot introduce threats to<br>th tit’ CDE||_(continued on next page)_|



|**Customized Approach Objective**|
|---|
|Devices that connect to untrusted environments and<br>also connect to the CDE cannot introduce threats to<br>the entity’s CDE.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 59_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Applicability Notes**|**Good Practice**|
|---|---|
|These security controls may be temporarily disabled<br>only if there is legitimate technical need, as<br>authorized by management on a case-by-case<br>basis. If these security controls need to be disabled<br>for a specific purpose, it must be formally<br>authorized. Additional security measures may also<br>need to be implemented for the period during which<br>these security controls are not active.|The specific configuration settings are determined<br>by the entity and should be consistent with its<br>network security policies and procedures.<br>Where there is a legitimate need to temporarily<br>disable security controls on a company-owned or<br>employee-owned device that connects to both an<br>untrusted network and the CDE—for example, to<br>support a specific maintenance activity or<br>investigation of a technical problem—the reason|
|This requirement applies to employee-owned and<br>company-owned computing devices. Systems that<br>cannot be managed by corporate policy introduce<br>weaknesses and provide opportunities that<br>malicious individuals may exploit.|for taking such action is understood and approved<br>by an appropriate management representative.<br>Any disabling or altering of these security<br>controls, including on administrators’ own<br>devices, is performed by authorized personnel.<br>It is recognized that administrators have privileges<br>that may allow them to disable security controls<br>on their own computers, but there should be<br>alerting mechanisms in place when such controls<br>are disabled and follow up that occurs to ensure<br>processes were followed.<br>**Examples**<br>Practices include forbidding split-tunneling of<br>VPNs for employee-owned or corporate-owned<br>mobile devices and requiring that such devices<br>boot up into a VPN.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 60_ 



#### **_Requirement 2: Apply Secure Configurations to All System Components_** 

###### **Sections** 

- **2.1** Processes and mechanisms for applying secure configurations to all system components are defined and understood. 

- **2.2** System components are configured and managed securely. 

- **2.3** Wireless environments are configured and managed securely. 

###### **Overview** 

Malicious individuals, both external and internal to an entity, often use default passwords and other vendor default settings to compromise systems. These passwords and settings are well known and are easily determined via public information. 

Applying secure configurations to system components reduces the means available to an attacker to compromise the system. Changing default passwords, removing unnecessary software, functions, and accounts, and disabling or removing unnecessary services all help to reduce the potential attack surface. 

Refer to _Appendix G_ for definitions of PCI DSS terms. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 61_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **2.1 Processes and mechanisms for applying secure configurations to all system components are defined and understood.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**2.1.1**All security policies and operational<br>procedures that are identified in Requirement 2 are:<br>•<br>Documented.<br>•<br>Kept up to date.<br>•<br>In use.<br>•<br>Known to all affected parties.|**2.1.1**Examine documentation and interview<br>personnel to verify that security policies and<br>operational procedures identified in Requirement 2<br>are managed in accordance with all elements<br>specified in this requirement.|Requirement 2.1.1 is about effectively managing<br>and maintaining the various policies and<br>procedures specified throughout Requirement 2.<br>While it is important to define the specific policies<br>or procedures called out in Requirement 2, it is<br>equally important to ensure they are properly<br>documented, maintained, and disseminated.<br>**Good Practice**|
|**Customized Approach Objective**||It is important to update policies and procedures<br>as needed to address changes in processes,|
|Expectations, controls, and oversight for meeting<br>activities within Requirement 2 are defined and<br>adhered to by affected personnel. All supporting<br>activities are repeatable, consistently applied, and<br>conform to management’s intent.||technologies, and business objectives. For this<br>reason, consider updating these documents as<br>soon as possible after a change occurs and not<br>only on a periodic cycle<br>**Definitions**<br>Security policies define the entity’s security<br>objectives and principles.<br>Operational procedures describe how to perform<br>activities, and define the controls, methods, and<br>processes that are followed to achieve the<br>desired result in a consistent manner and in<br>accordance with policy objectives.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 62_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**2.1.2**Roles and responsibilities for performing<br>activities in Requirement 2 are documented,<br>assigned, and understood.|**2.1.2.a**Examine documentation to verify that<br>descriptions of roles and responsibilities for<br>performing activities in Requirement 2 are<br>documented and assigned.|If roles and responsibilities are not formally<br>assigned, personnel may not be aware of their<br>day-to-day responsibilities and critical activities<br>may not occur.<br>**Good Practice**|
|**Customized Approach Objective**<br>Day-to-day responsibilities for performing all the<br>activities in Requirement 2 are allocated. Personnel<br>are accountable for successful, continuous<br>operation of these requirements.|**2.1.2.b**Interview personnel with responsibility for<br>performing activities in Requirement 2 to verify that<br>roles and responsibilities are assigned as<br>documented and are understood.|Roles and responsibilities may be documented<br>within policies and procedures or maintained<br>within separate documents.<br>As part of communicating roles and<br>responsibilities, entities can consider having<br>personnel acknowledge their acceptance and<br>understanding of their assigned roles and<br>responsibilities.<br>**Examples**<br>A method to document roles and responsibilities<br>is a responsibility assignment matrix that includes<br>who is responsible, accountable, consulted, and<br>informed (also called a RACI matrix).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 63_ 



**Requirements and Testing Procedures** 

###### **Guidance** 

**2.2 System components are configured and managed securely. Defined Approach Requirements Defined Approach Testing Procedures Purpose** There are known weaknesses with many **2.2.1** Configuration standards are developed, **2.2.1.a** Examine system configuration standards operating systems, databases, network devices, implemented, and maintained to: to verify they define processes that include all software, applications, container images, and • Cover all system components. elements specified in this requirement. other devices used by an entity or within an • Address all known security vulnerabilities. entity’s environment. There are also known ways • Be consistent with industry-accepted system **2.2.1.b** Examine policies and procedures and to configure these system components to fix interview personnel to verify that system security vulnerabilities. Fixing security hardening standards or vendor hardening configuration standards are updated as new vulnerabilities reduces the opportunities available recommendations. vulnerability issues are identified, as defined in to an attacker. • Be updated as new vulnerability issues are Requirement 6.3.1. By developing standards, entities ensure their identified, as defined in Requirement 6.3.1. system components will be configured • Be applied when new systems are configured **2.2.1.c** Examine configuration settings and consistently and securely and will address the and verified as in place before or immediately interview personnel to verify that system protection of devices for which full hardening may after a system component is connected to a configuration standards are applied when new be more difficult. production environment. systems are configured and verified as being in **Good Practice** place before or immediately after a system component is connected to a production Keeping up to date with current industry guidance **Customized Approach Objective** environment. will help the entity maintain secure configurations. The specific controls to be applied to a system will All system components are configured securely and vary and should be appropriate for the type and consistently and in accordance with industryfunction of the system. accepted hardening standards or vendor recommendations. Numerous security organizations have established system-hardening guidelines and recommendations, which advise how to correct common, known weaknesses. **Further Information** Sources for guidance on configuration standards include but are not limited to: Center for Internet Security (CIS), International Organization for Standardization (ISO), National Institute of Standards and Technology (NIST), Cloud Security Alliance, and product vendors. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 64_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**2.2.2**Vendor default accounts are managed as<br>follows:<br>•<br>If the vendor default account(s) will be used, the<br>default password is changed per Requirement|**2.2.2.a**Examine system configuration standards to<br>verify they include managing vendor default<br>accounts in accordance with all elements specified<br>in this requirement.|Malicious individuals often use vendor default<br>account names and passwords to compromise<br>operating systems, applications, and the systems<br>on which they are installed. Because these<br>default settings are often published and are well|
|8.3.6.<br>•<br>If the vendor default account(s) will not be used,<br>the account is removed or disabled.|**2.2.2.b**Examine vendor documentation and<br>observe a system administrator logging on using<br>vendor default accounts to verify accounts are<br>implemented in accordance with all elements<br>specified in this requirement.|known, changing these settings will make<br>systems less vulnerable to attack.<br>**Good Practice**<br>All vendor default accounts should be identified,<br>and their purpose and use understood. It is<br>important to establish controls for application and|
||**2.2.2.c**Examine configuration files and interview<br>personnel to verify that all vendor default accounts|system accounts, including those used to deploy<br>and maintain cloud services so that they do not|
|**Customized Approach Objective**|<br>that will not be used are removed or disabled.|use default passwords and are not usable by<br>unauthorized individuals.|
|System components cannot be accessed using<br>default passwords.||Where a default account is not intended to be<br>used, changing the default password to a unique<br>password that meets PCI DSS Requirement|
|**Applicability Notes**||8.3.6, removing any access to the default<br>account, and then disabling the account, will|
|This applies to ALL vendor default accounts and<br>passwords, including, but not limited to, those used<br>by operating systems, software that provides<br>security services, application and system accounts,<br>point-of-sale (POS) terminals, payment applications,<br>and Simple Network Management Protocol (SNMP)<br>defaults.<br>This reuirement also alies where a sstem||prevent a malicious individual from re-enabling<br>the account and gaining access with the default<br>password.<br>Using an isolated staging network to install and<br>configure new systems is recommended and can<br>also be used to confirm that default credentials<br>have not been introduced into production<br>environments.|



This requirement also applies where a system component is not installed within an entity’s environment, for example, software and applications that are part of the CDE and are accessed via a cloud subscription service. 

###### **Examples** 

Defaults to be considered include user IDs, passwords, and other authentication credentials commonly used by vendors in their products. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 65_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**2.2.3**Primary functions requiring different security<br>levels are managed as follows:<br>•<br>Only one primary function exists on a system<br>component,|**2.2.3.a**Examine system configuration standards to<br>verify they include managing primary functions<br>requiring different security levels as specified in<br>this requirement.|Systems containing a combination of services,<br>protocols, and daemons for their primary function<br>will have a security profile appropriate to allow<br>that function to operate effectively. For example,<br>systems that need to be directly connected to the|
|**OR**<br>•<br>Primary functions with differing security levels<br>that exist on the same system component are<br>isolated from each other,<br>|**2.2.3.b**Examine system configurations to verify<br>that primary functions requiring different security<br>levels are managed per one of the ways specified<br>in this requirement.|Internet would have a particular profile, like a<br>DNS server, web server, or an e-commerce<br>server. Conversely, other system components<br>may operate a primary function comprising a<br>different set of services, protocols, and daemons|
|**OR**||that perform functions that an entity does not want|
|•<br>Primary functions with differing security levels on<br>the same system component are all secured to<br>the level required by the function with the<br>highest security need.|**2.2.3.c**Where virtualization technologies are used,<br>examine the system configurations to verify that<br>system functions requiring different security levels<br>are managed in one of the following ways:|<br>exposed to the Internet. This requirement aims to<br>ensure that different functions do not impact the<br>security profiles of other services in a way which<br>may cause them to operate at a higher or lower|
||•<br>Functions with differing security needs do not|security level.|
|**Customized Approach Objective**|co-exist on the same system component.|**Good Practice**|
|Primary functions with lower security needs cannot<br>affect the security of primary functions with higher<br>security needs on the same system component.|•<br>Functions with differing security needs that<br>exist on the same system component are<br>isolated from each other.<br>•<br>Functions with differing security needs on the<br>same system component are all secured to the<br>level required by the function with the highest<br>security need.|Ideally, each function should be placed on<br>different system components. This can be<br>achieved by implementing only one primary<br>function on each system component. Another<br>option is to isolate primary functions on the same<br>system component that have different security<br>levels, for example, isolating web servers (which<br>need to be directly connected to the Internet) from<br>application and database servers.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 66_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**2.2.3**_(continued)_|If a system component contains primary functions<br>that need different security levels, a third option is<br>to implement additional controls to ensure that the<br>resultant security level of the primary function(s)<br>with higher security needs is not reduced by the<br>presence of the lower security primary functions.<br>Additionally, the functions with a lower security<br>level should be isolated and/or secured to ensure<br>they cannot access or affect the resources of<br>another system function, and do not introduce<br>security weaknesses to other functions on the<br>same server.|
||Functions of differing security levels may be<br>isolated by either physical or logical controls. For<br>example, a database system should not also be<br>hosting web services unless using controls like<br>virtualization technologies to isolate and contain<br>the functions into separate sub-systems. Another<br>example is using virtual instances or providing<br>dedicated memory access by system function.<br>Where virtualization technologies are used, the<br>security levels should be identified and managed<br>for each virtual component. Examples of<br>considerations for virtualized environments<br>include:|
||•<br>The function of each application, container, or<br>virtual server instance.|
||•<br>How virtual machines (VMs) or containers are<br>stored and secured.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 67_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**2.2.4**Only necessary services, protocols, daemons,<br>and functions are enabled, and all unnecessary<br>functionality is removed or disabled.<br>**Customized Approach Objective**<br>System components cannot be compromised by<br>exploiting unnecessary functionality present in the<br>system component.|**2.2.4.a**Examine system configuration standards to<br>verify necessary services, protocols, daemons, and<br>functions are identified and documented.<br>**2.2.4.b**Examine system configurations to verify the<br>following:<br>•<br>All unnecessary functionality is removed or<br>disabled.<br>•<br>Only required functionality, as documented in<br>the configuration standards, is enabled.|Unnecessary services and functions can provide<br>additional opportunities for malicious individuals<br>to gain access to a system. By removing or<br>disabling all unnecessary services, protocols,<br>daemons, and functions, organizations can focus<br>on securing the functions that are required and<br>reduce the risk that unknown or unnecessary<br>functions will be exploited.<br>**Good Practice**<br>There are many protocols that could be enabled<br>by default that are commonly used by malicious<br>individuals to compromise a network. Disabling or<br>removing all services, functions, and protocols<br>that are not used minimizes the potential attack<br>surface—for example, by removing or disabling<br>an unused FTP or web server.<br>**Examples**<br>Unnecessary functionality may include, but is not<br>limited to scripts, drivers, features, subsystems,<br>file systems, interfaces (USB and Bluetooth), and<br>unnecessary web servers.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 68_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**2.2.5**If any insecure services, protocols, or<br>daemons are present:<br>•<br>Business justification is documented.<br>•<br>Additional security features are documented and<br>implemented that reduce the risk of using<br>insecure services, protocols, or daemons.|**2.2.5.a**If any insecure services, protocols, or<br>daemons are present, examine system<br>configuration standards and interview personnel to<br>verify they are managed and implemented in<br>accordance with all elements specified in this<br>requirement.|Ensuring that all insecure services, protocols, and<br>daemons are adequately secured with<br>appropriate security features makes it more<br>difficult for malicious individuals to exploit<br>common points of compromise within a network.<br>**Good Practice**<br>Enabling security features before new system|
||**2.2.5.b**If any insecure services, protocols, or<br>daemons, are present, examine configuration|components are deployed will prevent insecure<br>configurations from being introduced into the|
|**Customized Approach Objective**|<br>settings to verify that additional security features<br>are implemented to reduce the risk of using|environment. Some vendor solutions may provide<br>additional security functions to assist with<br>|
|System components cannot be compromised by<br>exploiting insecure services, protocols, or daemons.|insecure services, daemons, and protocols.|securing an insecure process.<br>**Further Information**<br>For guidance on services, protocols, or daemons<br>considered to be insecure, refer to industry<br>standards and guidance (for example, as<br>published by NIST, ENISA, and OWASP).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 69_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**2.2.6**System security parameters are configured to<br>prevent misuse.<br>**Customized Approach Objective**|**2.2.6.a**Examine system configuration standards to<br>verify they include configuring system security<br>parameters to prevent misuse.<br>**2.2.6.b**Interview system administrators and/or<br>security managers to verify they have knowledge<br>of common security parameter settings for system<br>components.<br>**2.2.6.c**Examine system configurations to verify<br>that common security parameters are set<br>appropriately and in accordance with the system<br>configuration standards.|Correctly configuring security parameters<br>provided in system components takes advantage<br>of the capabilities of the system component to<br>defeat malicious attacks.<br>**Good Practice**<br>System configuration standards and related<br>processes should specifically address security<br>settings and parameters that have known security<br>implications for each type of system in use.<br>For systems to be configured securely, personnel<br>responsible for configuration and/or administering<br>systems should be knowledgeable in the specific<br>security parameters and settings that apply to the<br>system. Considerations should also include|
|System components cannot be compromised<br>because of incorrect security parameter<br>configuration.||secure settings for parameters used to access<br>cloud portals.<br>**Further Information**<br>Refer to vendor documentation and industry<br>references noted in Requirement 2.2.1 for<br>information about applicable security parameters<br>for each type of system.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 70_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**2.2.7**All non-console administrative access is<br>encrypted using strong cryptography.|**2.2.7.a**Examine system configuration standards to<br>verify they include encrypting all non-console<br>administrative access using strong cryptography.|If non-console (including remote) administration<br>does not use encrypted communications,<br>administrative authorization factors (such as IDs<br>and passwords) can be revealed to an<br>eavesdropper. A malicious individual could use|
||**2.2.7.b**Observe an administrator log on to system<br>components and examine system configurations to<br>verify that non-console administrative access is<br>managed in accordance with this requirement.|this information to access the network, become<br>administrator, and steal data.<br>**Good Practice**<br>Whichever security protocol is used, it should be<br>configured to use only secure versions and|
||**2.2.7.c**Examine settings for system components<br>and authentication services to verify that insecure<br>remote login services are not available for non-<br>console administrative access.|configurations to prevent use of an insecure<br>connection—for example, by using only trusted<br>certificates, supporting only strong encryption,<br>and not supporting fallback to weaker, insecure<br>protocols or methods.|
||**2.2.7.d**Examine vendor documentation and<br>interview personnel to verify that strong|**Examples**<br>Cleartext protocols (such as HTTP, telnet, etc.) do|
|**Customized Approach Objective**|<br>cryptography for the technology in use is<br>implemented according to industry best practices|not encrypt traffic or logon details, making it easy<br>for an eavesdropper to intercept this information.|
|Cleartext administrative authorization factors cannot<br>be read or intercepted from any network<br>transmissions.|<br>and/or vendor recommendations.|Non-console access may be facilitated by<br>technologies that provide alternative access to<br>systems, including but not limited to, out-of-band<br>(OOB), lights-out management (LOM), Intelligent|
|**Applicability Notes**||Platform Management Interface (IPMI), and<br>keyboard, video, mouse (KVM) switches with|
|This includes administrative access via browser-<br>based interfaces and application programming<br>interfaces (APIs).||remote capabilities. These and other non-console<br>access technologies and methods must be<br>secured with strong cryptography.<br>**Further Information**<br>Refer to industry standards and best practices<br>such as_NIST SP 800-52 and SP 800-57_.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 71_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **2.3 Wireless environments are configured and managed securely.** 

###### **Defined Approach Requirements Defined Approach Testing Procedures** 

- **2.3.1** For wireless environments connected to the CDE or transmitting account data, all wireless vendor defaults are changed at installation or are confirmed to be secure, including but not limited to: 

   - **2.3.1.a** Examine policies and procedures and interview responsible personnel to verify that processes are defined for wireless vendor defaults to either change them upon installation or to confirm them to be secure in accordance with all elements of this requirement. 

- Default wireless encryption keys. 

- Passwords on wireless access points. 

- SNMP defaults. 

- • Any other security-related wireless vendor defaults. 

- **2.3.1.b** Examine vendor documentation and observe a system administrator logging into wireless devices to verify: 

###### **Purpose** 

If wireless networks are not implemented with sufficient security configurations (including changing default settings), wireless sniffers can eavesdrop on the traffic, easily capture data and passwords, and easily enter and attack the network. 

###### **Good Practice** 

Wireless passwords should be constructed so that they are resistant to offline brute force attacks. 

- SNMP defaults are not used. 

- Default passwords/passphrases on wireless access points are not used. 

**2.3.1.c** Examine vendor documentation and wireless configuration settings to verify other **Customized Approach Objective** security-related wireless vendor defaults were changed, if applicable. Wireless networks cannot be accessed using vendor default passwords or default configurations. 

###### **Applicability Notes** 

This includes, but is not limited to, default wireless encryption keys, passwords on wireless access points, SNMP defaults, and any other securityrelated wireless vendor defaults. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 72_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**2.3.2**For wireless environments connected to the<br>CDE or transmitting account data, wireless<br>encryption keys are changed as follows:<br>•<br>Whenever personnel with knowledge of the key<br>leave the company or the role for which the<br>knowledge was necessary.<br>•<br>Whenever a key is suspected of or known to be<br>compromised.|**2.3.2**Interview responsible personnel and examine<br>key-management documentation to verify that<br>wireless encryption keys are changed in<br>accordance with all elements specified in this<br>requirement.|Changing wireless encryption keys whenever<br>someone with knowledge of the key leaves the<br>organization or moves to a role that no longer<br>requires knowledge of the key, helps keep<br>knowledge of keys limited to only those with a<br>business need to know.<br>Also, changing wireless encryption keys<br>whenever a key is suspected or known to be<br>comprised makes a wireless network more<br>resistant to compromise.|
|**Customized Approach Objective**||**Good Practice**|
|Knowledge of wireless encryption keys cannot allow<br>unauthorized access to wireless networks.||This goal can be accomplished in multiple ways,<br>including periodic changes of keys, changing keys<br>via a defined “joiners-movers-leavers” (JML)<br>process, implementing additional technical<br>controls, and not using fixed pre-shared keys.<br>In addition, any keys that are known to be, or<br>suspected of being, compromised should be<br>managed in accordance with the entity’s incident<br>response plan at Requirement 12.10.1.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 73_ 



### **Protect Account Data** 

#### **_Requirement 3: Protect Stored Account Data_** 

###### **Sections** 

- **3.1** Processes and mechanisms for protecting stored account data are defined and understood. 

- **3.2** Storage of account data is kept to a minimum. 

- **3.3** Sensitive authentication data (SAD) is not stored after authorization. 

- **3.4** Access to displays of full PAN and ability to copy PAN are restricted. 

- **3.5** Primary account number (PAN) is secured wherever it is stored. 

- **3.6** Cryptographic keys used to protect stored account data are secured. 

- **3.7** Where cryptography is used to protect stored account data, key management processes and procedures covering all aspects of the key lifecycle are defined and implemented. 

###### **Overview** 

Protection methods such as encryption, truncation, masking, and hashing are critical components of account data protection. If an intruder circumvents other security controls and gains access to encrypted account data, the data is unreadable without the proper cryptographic keys and is unusable to that intruder. Other effective methods of protecting stored data should also be considered as potential risk-mitigation opportunities. For example, methods for minimizing risk include not storing account data unless necessary, truncating cardholder data if full PAN is not needed, and not sending unprotected PANs using end-user messaging technologies such as e-mail and instant messaging. 

If account data is present in non-persistent memory (for example, RAM, volatile memory), encryption of PAN is not required. However, proper controls must be in place to ensure that memory maintains a non-persistent state. Data should be removed from volatile memory once the business purpose (for example, the associated transaction) is complete. In the case that data storage becomes persistent, all applicable PCI DSS Requirements will apply including encryption of stored data. 

Requirement 3 applies to protection of stored account data unless specifically called out in an individual requirement. 

Refer to _Appendix G_ for definitions of “strong cryptography” and other PCI DSS terms. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 74_ 



###### **Requirements and Testing Procedures Guidance** 

###### **3.1 Processes and mechanisms for protecting stored account data are defined and understood.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**3.1.1**All security policies and operational procedures<br>that are identified in Requirement 3 are:<br>•<br>Documented.<br>•<br>Kept up to date.<br>•<br>In use.|**3.1.1**Examine documentation and interview<br>personnel to verify that security policies and<br>operational procedures identified in Requirement 3<br>are managed in accordance with all elements<br>specified in this requirement.|Requirement 3.1.1 is about effectively managing and<br>maintaining the various policies and procedures<br>specified throughout Requirement 3. While it is<br>important to define the specific policies or procedures<br>called out in Requirement 3, it is equally important to<br>ensure they are properly documented, maintained, and<br>disseminated.|
|•<br>Known to all affected parties.||**Good Practice**|
|**Customized Approach Objective**||It is important to update policies and procedures as<br>needed to address changes in processes, technologies,|
|Expectations, controls, and oversight for meeting<br>activities within Requirement 3 are defined and adhered<br>to by affected personnel. All supporting activities are<br>repeatable, consistently applied, and conform to<br>management’s intent.||and business objectives. For this reason, consider<br>updating these documents as soon as possible after a<br>change occurs and not only on a periodic cycle.<br>**Definitions**<br>Security policies define the entity’s security objectives<br>and principles. Operational procedures describe how to<br>perform activities, and define the controls, methods,<br>and processes that are followed to achieve the desired<br>result in a consistent manner and in accordance with<br>policy objectives.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 75_ 



|**Requirements and Te**|**sting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.1.2**Roles and responsibilities for performing activities<br>in Requirement 3 are documented, assigned, and<br>understood.|**3.1.2.a**Examine documentation to verify that<br>descriptions of roles and responsibilities<br>performing activities in Requirement 3 are<br>documented and assigned.|If roles and responsibilities are not formally assigned,<br>personnel may not be aware of their day-to-day<br>responsibilities, and critical activities may not occur.<br>**Good Practice**<br>Roles and responsibilities may be documented within|
||**3.1.2.b**Interview personnel with responsibility for<br>performing activities in Requirement 3 to verify that|policies and procedures or maintained within separate<br>documents.|
|**Customized Approach Objective**|<br>roles and responsibilities are assigned as<br>documented and are understood.|As part of communicating roles and responsibilities,<br>entities can consider having personnel acknowledge|
|Day-to-day responsibilities for performing all the<br>activities in Requirement 3 are allocated. Personnel are<br>accountable for successful, continuous operation of<br>these requirements.||their acceptance and understanding of their assigned<br>roles and responsibilities.<br>**Examples**<br>A method to document roles and responsibilities is a<br>responsibility assignment matrix that includes who is<br>responsible, accountable, consulted, and informed<br>(also called a RACI matrix).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 76_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **3.2 Storage of account data is kept to a minimum.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|
|---|---|
|**3.2.1**Account data storage is kept to a minimum through<br>implementation of data retention and disposal policies,<br>procedures, and processes that include at least the<br>following:<br>•<br>Coverage for all locations of stored account data.|**3.2.1.a**Examine the data retention and disposal<br>policies, procedures, and processes and interview<br>personnel to verify processes are defined to<br>include all elements specified in this requirement.|
|•<br>Coverage for any sensitive authentication data (SAD)<br>stored prior to completion of authorization._This bullet_<br>_is a best practice until its effective date; refer to_<br>_Applicability Notes below for details._<br>•<br>Limiting data storage amount and retention time to|**3.2.1.b**Examine files and system records on<br>system components where account data is stored<br>to verify that the data storage amount and retention<br>time does not exceed the requirements defined in<br>the data retention policy.|
|that which is required for legal or regulatory, and/or<br>business requirements.<br>•<br>Specific retention requirements for stored account<br>|**3.2.1.c**Observe the mechanisms used to render<br>account data unrecoverable to verify data cannot<br>be recovered.|



- Specific retention requirements for stored account data that defines length of retention period and includes a documented business justification. 

- Processes for secure deletion or rendering account data unrecoverable when no longer needed per the retention policy. 

- A process for verifying, at least once every three months, that stored account data exceeding the defined retention period has been securely deleted or rendered unrecoverable. 

**Customized Approach Objective** Account data is retained only where necessary and for the least amount of time needed and is securely deleted or rendered unrecoverable when no longer needed. 

###### **Purpose** 

A formal data retention policy identifies what data needs to be retained, for how long, and where that data resides so it can be securely destroyed or deleted as soon as it is no longer needed. The only account data that may be stored after authorization is the primary account number or PAN (rendered unreadable), expiration date, cardholder name, and service code. The storage of SAD data prior to the completion of the authorization process is also included in the data retention and disposal policy so that storage of this sensitive data is kept to minimum, and only retained for the defined amount of time. 

###### **Good Practice** 

When identifying locations of stored account data, consider all processes and personnel with access to the data, as data could have been moved and stored in different locations than originally defined. Storage locations that are often overlooked include backup and archive systems, removable data storage devices, paper-based media, and audio recordings. 

To define appropriate retention requirements, an entity first needs to understand its own business needs as well as any legal or regulatory obligations that apply to its industry or to the type of data being retained. Implementing an automated process to ensure data is automatically and securely deleted upon its defined retention limit can help ensure that account data is not retained beyond what is necessary for business, legal, or regulatory purposes. _(continued on next page)_ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 77_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Applicability Notes**<br>Where account data is stored by a TPSP (for example,<br>in a cloud environment), entities are responsible for<br>working with their service providers to understand how<br>the TPSP meets this requirement for the entity.<br>Considerations include ensuring that all geographic<br>instances of a data element are securely deleted.|Methods of eliminating data when it exceeds the<br>retention period include secure deletion to complete<br>removal of the data or rendering it unrecoverable and<br>unable to be reconstructed. Identifying and securely<br>eliminating stored data that has exceeded its specified<br>retention period prevents unnecessary retention of data<br>that is no longer needed. This process may be<br>automated, manual, or a combination of both.|
|_The bullet above (for coverage of SAD stored prior to_<br>_completion of authorization) is a best practice until 31_<br>_March 2025, after which it will be required as part of_<br>_Requirement 3.2.1 and must be fully considered during a_<br>_PCI DSS assessment._|The deletion function in most operating systems is not<br>“secure deletion” as it allows deleted data to be<br>recovered, so instead, a dedicated secure deletion<br>function or application must be used to make data<br>unrecoverable.|
||_Remember, if you don't need it, don't store it!_<br>**Examples**<br>An automated, programmatic procedure could be run to<br>locate and remove data, or a manual review of data<br>storage areas could be performed. Whichever method<br>is used, it is a good idea to monitor the process to<br>ensure it is completed successfully, and that the results<br>are recorded and validated as being complete.<br>Implementing secure deletion methods ensures that the<br>data cannot be retrieved when it is no longer needed.<br>**Further Information**<br>See_NIST SP 800-88 Rev. 1,_ _Guidelines for Media_<br>_Sanitization_.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 78_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **3.3 Sensitive authentication data (SAD) is not stored after authorization.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**3.3.1**SAD is not stored after authorization, even if<br>encrypted. All sensitive authentication data received is<br>rendered unrecoverable upon completion of the<br>authorization process.|**3.3.1.a**If SAD is received, examine documented<br>policies, procedures, and system configurations to<br>verify the data is not stored after authorization.|SAD is very valuable to malicious individuals as it<br>allows them to generate counterfeit payment cards and<br>create fraudulent transactions. Therefore, the storage<br>of SAD upon completion of the authorization process is<br>prohibited.|
||**3.3.1.b**If SAD is received, examine the|**Good Practice**|
|**Customized Approach Objective**<br>This requirement is not eligible for the customized<br>approach.|documented procedures and observe the secure<br>data deletion processes to verify the data is<br>rendered unrecoverable upon completion of the<br>authorization process.|It may be acceptable for an entity to store SAD in non-<br>persistent memory for a short time after authorization is<br>complete, if following conditions are met:<br>•<br>There is a legitimate business need to access<br>SAD in memory after authorization is complete.|
|**Applicability Notes**||•<br>SAD is only ever stored in non-persistent memory<br>(for example, RAM, volatile memory).|
|Issuers and companies that support issuing services,<br>where there is a legitimate and documented business<br>need to store SAD, are not required to meet this<br>requirement. A legitimate business need is one that is<br>necessary for the performance of the function being<br>provided by or for the issuer. Refer to Requirement 3.3.3||•<br>Controls are in place to ensure that memory<br>maintains a non-persistent state.<br>•<br>SAD is removed as soon as the business purpose<br>is complete.<br>It is not permissible to store SAD in persistent memory.<br>**Definitions**|
|for additional requirements specifically for these entities.<br>Sensitive authentication data includes the data cited in<br>Requirements 3.3.1.1 through 3.3.1.3.||The authorization process completes when a merchant<br>receives a transaction response (for example, an<br>approval or decline).<br>Refer to_Appendix G_for the definition of “authorization.”|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 79_ 



|**Requirements and Te**|**sting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.3.1.1**The full contents of any track are not stored upon<br>completion of the authorization process.<br>**Customized Approach Objective**|**3.3.1.1**Examine data sources to verify that the full<br>contents of any track are not stored upon<br>completion of the authorization process.|If full contents of any track (from the magnetic stripe on<br>the back of a card if present, equivalent data contained<br>on a chip, or elsewhere) is stored, malicious individuals<br>who obtain that data can use it to reproduce payment<br>cards and complete fraudulent transactions.|
|This requirement is not eligible for the customized<br>approach.||**Definitions**<br>Full track data is alternatively called full track, track,<br>track 1, track 2, and magnetic-stripe data. Each track|
|**Applicability Notes**||contains a number of data elements, and this<br>requirement specifies only those that may be retained|
|In the normal course of business, the following data<br>elements from the track may need to be retained:||post-authorization.<br>**Examples**|
|•<br>Cardholder name.<br>•<br>Primary account number (PAN).<br>•<br>Expiration date.<br>•<br>Service code.<br>To minimize risk, store securely only these data<br>elements as needed for business.||Data sources to review to ensure that the full contents<br>of any track are not retained upon completion of the<br>authorization process include, but are not limited to:<br>•<br>Incoming transaction data.<br>•<br>All logs (for example, transaction, history,<br>debugging, error).<br>•<br>History files.<br>•<br>Trace files.<br>•<br>Database schemas.<br>•<br>Contents of databases, and on-premise and cloud<br>data stores.<br>•<br>Any existing memory/crash dump files.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 80_ 



|**Requirements and Te**|**sting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.3.1.2**The card verification code is not stored upon<br>completion of the authorization process.|**3.3.1.2**Examine data sources, to verify that the<br>card verification code is not stored upon<br>completion of the authorization process.|If card verification code data is stolen, malicious<br>individuals can execute fraudulent Internet and mail-<br>order/telephone-order (MO/TO) transactions. Not<br>storing this data reduces the probability of it being|
|**Customized Approach Objective**||compromised.|
|This requirement is not eligible for the customized<br>approach.<br>**Applicability Notes**||**Examples**<br>If card verification codes are stored on paper media<br>prior to completion of authorization, a method of<br>erasing or covering the codes should prevent them<br>from being read after authorization is complete.<br>Example methods of rendering the codes unreadable|
|The card verification code is the three- or four-digit<br>number printed on the front or back of a payment card<br>used to verify card-not-present transactions.||include removing the code with scissors and applying a<br>suitably opaque and un-removable marker over the<br>code.<br>Data sources to review to ensure that the card<br>verification code is not retained upon completion of the<br>authorization process include, but are not limited to:<br>•<br>Incoming transaction data.<br>•<br>All logs (for example, transaction, history,<br>debugging, error).<br>•<br>History files.<br>•<br>Trace files.<br>•<br>Database schemas.<br>•<br>Contents of databases, and on-premise and cloud<br>data stores.|
|||•<br>Any existing memory/crash dump files.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 81_ 



|**Requirements and Te**|**sting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.3.1.3**The personal identification number (PIN) and the<br>PIN block are not stored upon completion of the<br>authorization process.|**3.3.1.3**Examine data sources, to verify that PINs<br>and PIN blocks are not stored upon completion of<br>the authorization process.|PIN and PIN blocks should be known only to the card<br>owner or entity that issued the card. If this data is<br>stolen, malicious individuals can execute fraudulent<br>PIN-based transactions (for example, in-store|
|**Customized Approach Objective**||purchases and ATM withdrawals). Not storing this data<br>reduces the probability of it being compromised.|
|This requirement is not eligible for the customized<br>approach.||**Examples**<br>Data sources to review to ensure that PIN and PIN<br>blocks are not retained upon completion of the|
|**Applicability Notes**<br>PIN blocks are encrypted during the natural course of<br>transaction processes, but even if an entity encrypts the<br>PIN block again, it is still not allowed to be stored after<br>the completion of the authorization process.||authorization process include, but are not limited to:<br>•<br>Incoming transaction data.<br>•<br>All logs (for example, transaction, history,<br>debugging, error).<br>•<br>History files.<br>•<br>Trace files.<br>•<br>Database schemas.<br>•<br>Contents of databases, and on-premise and cloud<br>data stores.<br>•<br>Any existing memory/crash dump files.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 82_ 



|**Requirements and Te**|**sting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.3.2**SAD that is stored electronically prior to completion<br>of authorization is encrypted using strong cryptography.<br>**Customized Approach Objective**<br>This requirement is not eligible for the customized<br>approach.<br>_(continued on next page)_|**3.3.2**Examine data stores, system configurations,<br>and/or vendor documentation to verify that all SAD<br>that is stored electronically prior to completion of<br>authorization is encrypted using strong<br>cryptography.|SAD can be used by malicious individuals to increase<br>the probability of successfully generating counterfeit<br>payment cards and creating fraudulent transactions.<br>**Good Practice**<br>Entities should consider encrypting SAD with a different<br>cryptographic key than is used to encrypt PAN. Note<br>that this does not mean that PAN present in SAD (as<br>part of track data) would need to be separately<br>encrypted.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 83_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Applicability Notes**<br>Whether SAD is permitted to be stored prior to<br>authorization is determined by the organizations that<br>manage compliance programs (for example, payment<br>brands and acquirers). Contact these organizations for<br>any additional criteria.|**Definitions**<br>The authorization process is completed when a<br>merchant receives a transaction response (for example,<br>an approval or decline) .<br>Refer to_Appendix G_for the definition of “authorization.”|
|This requirement applies to all storage of SAD, even if<br>no PAN is present in the environment.||
|Refer to Requirement 3.2.1 for an additional requirement<br>that applies if SAD is stored prior to completion of<br>authorization.||
|Issuers and companies that support issuing services,<br>where there is a legitimate and documented business<br>need to store SAD,  are not required to meet this<br>requirement. A legitimate business need is one that is<br>necessary for the performance of the function being<br>provided by or for the issuer.||
|Refer to Requirement 3.3.3 for requirements specifically<br>for these entities.||
|This requirement does not replace how PIN blocks are<br>required to be managed, nor does it mean that a<br>properly encrypted PIN block needs to be encrypted<br>again.||
|_This requirement is a best practice until 31 March 2025,_<br>_after which it will be required and must be fully_<br>_considered during a PCI DSS assessment._||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 84_ 



|**Requirements and Te**|**sting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.3.3** **_Additional requirement for issuers and_**<br>**_companies that support issuing services and store_**<br>**_sensitive authentication data:_**Any storage of sensitive<br>authentication data is:<br>•<br>Limited to that which is needed for a legitimate<br>issuing business need and is secured.<br>•<br>Encrypted using strong cryptography._This bullet is a_<br>_best practice until its effective date; refer to_<br>_Applicability Notes below for details._|**3.3.3.a** **_Additional testing procedure for issuers_**<br>**_and companies that support issuing services_**<br>**_and store sensitive authentication data:_**<br>Examine documented policies and interview<br>personnel to verify there is a documented business<br>justification for the storage of sensitive<br>authentication data.<br>**3.3.3.b** **_Additional testing procedure for issuers_**<br>**_and companies that support issuing services_**|SAD can be used by malicious individuals to increase<br>the probability of successfully generating counterfeit<br>payment cards and creating fraudulent transactions**.**<br>**Good Practice**<br>Entities should consider encrypting SAD with a different<br>cryptographic key than is used to encrypt PAN. Note<br>that this does not mean that PAN present in SAD (as<br>part of track data) would need to be separately<br>encrypted.|
|**Customized Approach Objective**<br>Sensitive authentication data is retained only as required<br>to support issuing functions and is secured from<br>unauthorized access.|**_and store sensitive authentication data:_**<br>Examine data stores and system configurations to<br>verify that the sensitive authentication data is<br>stored securely.||
|_(continued on next page)_|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024_ 

_Page 85_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Applicability Notes**||
|This requirement applies only to issuers and companies<br>that support issuing services and store sensitive<br>authentication data.||
|Entities that issue payment cards or that perform or<br>support issuing services will often create and control<br>sensitive authentication data as part of the issuing<br>function. It is allowable for companies that perform,<br>facilitate, or support issuing services to store sensitive<br>authentication data ONLY IF they have a legitimate<br>business need to store such data.||
|A legitimate issuing business need is one that is<br>necessary for the performance of the function being<br>provided by or for the issuer.||
|_The bullet above (for encrypting stored SAD with strong_<br>_cryptography) is a best practice until 31 March 2025,_<br>_after which it will be required as part of Requirement_<br>_3.3.3 and must be fully considered during a PCI DSS_<br>_assessment._||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 86_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **3.4 Access to displays of full PAN and ability to copy PAN are restricted.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**3.4.1**PAN is masked when displayed (the BIN and last<br>four digits**are the maximum number**of digits to be<br>displayed), such that only personnel with a legitimate<br>business need can see**more than**the BIN and last four<br>digits of the PAN.|**3.4.1.a**Examine documented policies and<br>procedures for masking the display of PANs to<br>verify:<br>•<br>A list of roles that need access to more than<br>the BIN and last four digits of the PAN|The display of full PAN on computer screens, payment<br>card receipts, paper reports, etc. can result in this data<br>being obtained by unauthorized individuals and used<br>fraudulently. Ensuring that the full PAN is displayed<br>only for those with a legitimate business need<br>minimizes the risk of unauthorized persons gaining|
|_(continued on next page)_|(includes full PAN) is documented, together<br>with a legitimate business need for each role<br>to have such access.<br>•<br>PAN is masked when displayed such that only<br>personnel with a legitimate business need can<br>see more than the BIN and last four digits of<br>the PAN.<br>•<br>All roles not specifically authorized to see the<br>full PAN must only see masked PANs.|access to PAN data.<br>**Good Practice**<br>Applying access controls according to defined roles is<br>one way to limit access to viewing full PAN to only<br>those individuals with a defined business need.<br>The masking approach should always display only the<br>number of digits needed to perform a specific business<br>function. For example, if only the last four digits are<br>needed to perform a business function, PAN should be|
||**3.4.1.b**Examine system configurations to verify<br>that full PAN is only displayed for roles with a<br>documented business need, and that PAN is<br>masked for all other requests.|masked to only show the last four digits. As another<br>example, if a function needs to view the bank<br>identification number (BIN) for routing purposes,<br>unmask only the BIN digits for that function.<br>_(continued on next page)_|
||**3.4.1.c**Examine displays of PAN (for example, on<br>screen, on paper receipts) to verify that PANs are<br>masked when displayed, and that only those with a<br>legitimate business need are able to see more than<br>the BIN and/or last four digits of the PAN.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 87_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Customized Approach Objective**|**Definitions**|
|PAN displays are restricted to the minimum number of<br>digits necessary to meet a defined business need.|Masking is not synonymous with truncation and these<br>terms cannot be used interchangeably. Masking refers<br>to the concealment of certain digits during display or<br>printing, even when the entire PAN is stored on a<br>system. This is different from truncation, in which the<br>truncated digits are removed and cannot be retrieved<br>within the system. Masked PAN could be “unmasked”,|
|**Applicability Notes**|but there is no "un-truncation" without recreating the<br>PAN from another source.|
|This requirement does not supersede stricter<br>requirements in place for displays of cardholder data—<br>for example, legal or payment brand requirements for<br>point-of-sale (POS) receipts.|Refer to_Appendix G_for definitions of “masking” and<br>“truncation.”<br>**Further Information**|
|This requirement relates to protection of PAN where it is<br>displayed on screens, paper receipts, printouts, etc., and<br>is not to be confused with Requirement 3.5.1 for|For more information about masking and truncation,<br>see PCI SSC’s FAQs on these topics_._|
|protection of PAN when stored, processed, or<br>transmitted.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 88_ 



|**Requirements and Te**|**sting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.4.2**When using remote-access technologies, technical<br>controls prevent copy and/or relocation of PAN for all<br>personnel, except for those with documented, explicit<br>authorization and a legitimate, defined business need.|**3.4.2.a**Examine documented policies and<br>procedures and documented evidence for technical<br>controls that prevent copy and/or relocation of PAN<br>when using remote-access technologies onto local<br>hard drives or removable electronic media to verify|Relocation of PAN to unauthorized storage devices is a<br>common way for this data to be obtained and used<br>fraudulently.<br>Methods to ensure that only those with explicit<br>authorization and a legitimate business reason can|
|**Customized Approach Objective**|<br>the following:<br>|copy or relocate PAN minimizes the risk of<br>unauthorized persons gaining access to PAN.|
|PAN cannot be copied or relocated by unauthorized<br>personnel using remote-access technologies.|•<br>Technical controls prevent all personnel not<br>specifically authorized from copying and/or<br>relocating PAN.<br>•<br>A list of personnel with permission to copy<br>and/or relocate PAN is maintained, together<br>with the documented, explicit authorization and<br>legitimate, defined business need.|**Good Practice**<br>Copying and relocation of PAN should only be done to<br>storage devices that are permissible and authorized for<br>that individual.<br>**Definitions**<br>A virtual desktop is an example of a remote-access<br>|
|||technolo Such remote access technoloies often|
|**Applicability Notes**|**3.4.2.b**Examine configurations for remote-access<br>technologies to verify that technical controls to|gy.    g<br>include tools to disable copy and/or relocation<br>functionality.|
|Storing or relocating PAN onto local hard drives,<br>removable electronic media, and other storage devices<br>brings these devices into scope for PCI DSS.<br>_This requirement is a best practice until 31 March 2025,_<br>_after which it will be required and must be fully_<br>_considered during a PCI DSS assessment._|prevent copy and/or relocation of PAN for all<br>personnel, unless explicitly authorized.<br>**3.4.2.c**Observe processes and interview<br>personnel to verify that only personnel with<br>documented, explicit authorization and a<br>legitimate, defined business need have permission<br>to copy and/or relocate PAN when using remote-<br>access technologies.|Storage devices include, but are not limited to, local<br>hard drives, virtual drives, removable electronic media,<br>network drives, and cloud storage.<br>**Further Information**<br>Vendor documentation for the remote-access<br>technology in use will provide information about the<br>system settings needed to implement this requirement.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 89_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **3.5 Primary account number (PAN) is secured wherever it is stored.** 

###### **Defined Approach Requirements Defined Approach Testing Procedures** 

      - **3.5.1.a** Examine documentation about the system used to render PAN unreadable, including the vendor, type of system/process, and the encryption algorithms (if applicable) to verify that the PAN is rendered unreadable using any of the methods specified in this requirement. 

- **3.5.1** PAN is rendered unreadable anywhere it is stored by using any of the following approaches: 

- One-way hashes based on strong cryptography of the entire PAN. 

- Truncation (hashing cannot be used to replace the truncated segment of PAN). 

   - If hashed and truncated versions of the same PAN, or different truncation formats of the same PAN, are present in an environment, additional controls are in place such that the different versions cannot be correlated to reconstruct the original PAN. 

- **3.5.1.b** Examine data repositories and audit logs, including payment application logs, to verify the PAN is rendered unreadable using any of the methods specified in this requirement. 

**3.5.1.c** If hashed and truncated versions of the same PAN are present in the environment, examine implemented controls to verify that the hashed and truncated versions cannot be correlated to reconstruct the original PAN. 

- Index tokens. 

- Strong cryptography with associated keymanagement processes and procedures. 

###### **Customized Approach Objective** 

Cleartext PAN cannot be read from storage media. 

###### **Applicability Notes** 

This requirement applies to PANs stored in primary storage (databases, or flat files such as text files spreadsheets) as well as non-primary storage (backup, audit logs, exception, or troubleshooting logs). 

This requirement does not preclude the use of temporary files containing cleartext PAN while encrypting and decrypting PAN. 

###### **Purpose** 

Rendering stored PAN unreadable is a defense in depth control designed to protect the data if an unauthorized individual gains access to stored data by taking advantage of a vulnerability or misconfiguration of an entity’s primary access control. 

###### **Good Practice** 

It is a relatively trivial effort for a malicious individual to reconstruct original PAN data if they have access to both the truncated and hashed versions of a PAN. Controls that prevent the correlation of this data will help ensure that the original PAN remains unreadable. Implementing keyed cryptographic hashes with associated key management processes and procedures in accordance with Requirement 3.5.1.1 is a valid additional control to prevent correlation. 

###### **Further Information** 

For information about truncation formats and truncation in general, see PCI SSC’s FAQs on the topic. Sources for information about index tokens include: 

- PCI SSC’s Tokenization Product Security Guidelines ( _https://www.pcisecuritystandards.org/documents/T okenization_Product_Security_Guidelines.pdf_ ) 

- _ANSI X9.119-2-2017: Retail Financial Services - Requirements For Protection Of Sensitive Payment Card Data - Part 2: Implementing Post-Authorization Tokenization Systems_ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 90_ 



|**Requirements and Te**|**sting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.5.1.1**Hashes used to render PAN unreadable (per the<br>first bullet of Requirement 3.5.1) are keyed cryptographic<br>hashes of the entire PAN, with associated key-<br>management processes and procedures in accordance<br>with Requirements 3.6 and 3.7.|**3.5.1.1.a**Examine documentation about the<br>hashing method used to render PAN unreadable,<br>including the vendor, type of system/process, and<br>the encryption algorithms (as applicable) to verify<br>that the hashing method results in keyed<br>cryptographic hashes of the entire PAN, with<br>associated key management processes and|Rendering stored PAN unreadable is a defense in<br>depth control designed to protect the data if an<br>unauthorized individual gains access to stored data by<br>taking advantage of a vulnerability or misconfiguration<br>of an entity’s primary access control.<br>A hashing function that incorporates a randomly<br>generated secret key provides brute force attack|
|**Customized Approach Objective**|<br>procedures.|resistance and secret authentication integrity.<br>**Definitions**|
|Cleartext PAN cannot be determined from hashes of the<br>PAN.|**3.5.1.1.b**Examine documentation about the key<br>management procedures and processes<br>associated with the keyed cryptographic hashes to<br>verify keys are managed in accordance with<br>Requirements 3.6 and 3.7.|Refer to_Appendix G_for the definition of “keyed<br>cryptographic hash” and for information about<br>appropriate keyed cryptographic hashing algorithms<br>and additional resources.<br>**Examples**|
||**3.5.1.1.c**Examine data repositories to verify the<br>PAN is rendered unreadable.|Systems which only have access to one hash value at<br>a time and which store no other account data on the<br>same system as the hash, are not required to meet|
||**3.5.1.1.d**Examine audit logs, including payment<br>application logs, to verify the PAN is rendered<br>unreadable.|key-management processes and procedures<br>(Requirements 3.6 and 3.7). Examples of such systems<br>include transaction-originating devices that generate a<br>hash of the PAN for use in a backend system, such as|
|**Applicability Notes**||pay-at-gate transit turnstiles. However, in such an<br>implementation, the backend system will have access|
|All Applicability Notes for Requirement 3.5.1 also apply<br>to this requirement.<br>_(continued on next page)_||to more than one hash value at a time, and therefore is<br>required to meet key-management processes and<br>procedures at Requirements 3.6 and 3.7.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 91_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|_(continued)_||
|Key-management processes and procedures<br>(Requirements 3.6 and 3.7) do not apply to system<br>components used to generate individual keyed hashes<br>of a PAN for comparison to another system if:||
|•<br>The system components only have access to one<br>hash value at a time (hash values are not stored on<br>the system)<br>**AND**||
|•<br>There is no other account data stored on the same<br>system as the hashes.||
|_This requirement is considered a best practice until 31_<br>_March 2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment. This_<br>_requirement will replace the bullet in Requirement 3.5.1_<br>_for one-way hashes once its effective date is reached._||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 92_ 



|**Requirements and Te**|**sting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.5.1.2**If disk-level or partition-level encryption (rather<br>than file-, column-, or field-level database encryption) is<br>used to render PAN unreadable, it is implemented only<br>as follows:|**3.5.1.2.a**Examine encryption processes to verify<br>that, if disk-level or partition-level encryption is<br>used to render PAN unreadable, it is implemented<br>only as follows:|Disk-level and partition-level encryption typically<br>encrypts the entire disk or partition using the same key,<br>with all data automatically decrypted when the system<br>runs or when an authorized user requests it. For this<br>reason, disk-level encryption is not appropriate to|
|•<br>On removable electronic media<br>**OR**<br>•<br>If used for non-removable electronic media, PAN is<br>also rendered unreadable via another mechanism<br>that meets Requirement 3.5.1.|•<br>On removable electronic media,<br>**OR**<br>•<br>If used for non-removable electronic media,<br>examine encryption processes used to verify<br>that PAN is also rendered unreadable via<br>another method that meets Requirement 3.5.1.<br>**3.5.1.2.b**Examine configurations and/or vendor<br>documentation and observe encryption processes|protect stored PAN on computers, laptops, servers,<br>storage arrays, or any other system that provides<br>transparent decryption upon user authentication.<br>**Further Information**<br>Where available, following vendors’ hardening and<br>industry best practice guidelines can assist in securing<br>PAN on these devices.|
|**Customized Approach Objective**|to verify the system is configured according to<br>vendor documentation the result is that the disk or||
|Encrypted PAN is only decrypted when there is a<br>legitimate business need to access that PAN.<br>_(continued on next page)_|the partition is rendered unreadable.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 93_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Applicability Notes**||
|_(continued)_||
|This requirement applies to any encryption method that<br>provides clear-text PAN automatically when a system<br>runs, even though an authorized user has not<br>specifically requested that data.||
|While disk or partition encryption may still be present on<br>these types of devices, it cannot be the only mechanism<br>used to protect PAN stored on those systems. Any<br>stored PAN must also be rendered unreadable per<br>Requirement 3.5.1—for example, through truncation or a<br>data-level encryption mechanism. Full disk encryption<br>helps to protect data in the event of physical loss of a<br>disk and therefore its use is appropriate only for<br>removable electronic media storage devices.<br>Media that is part of a data center architecture (for<br>example, hot-swappable drives, bulk tape-backups) is<br>considered non-removable electronic media to which<br>Requirement 3.5.1 applies.||
|Disk or partition encryption implementations must also<br>meet all other PCI DSS encryption and key-management<br>requirements.<br>For issuers and companies that support issuing services:<br>This requirement does not apply to PANs being<br>accessed for real-time transaction processing. However,<br>it does apply to PANs stored for other purposes.||
|_This requirement is a best practice until 31 March 2025,_<br>_after which it will be required and must be fully_<br>_considered during a PCI DSS assessment._||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 94_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**3.5.1.3**If disk-level or partition-level encryption is used<br>(rather than file-, column-, or field-level database<br>encryption) to render PAN unreadable, it is managed as<br>follows:<br>•<br>Logical access is managed separately and<br>independently of native operating system|**3.5.1.3.a**If disk-level or partition-level encryption is<br>used to render PAN unreadable, examine the<br>system configuration and observe the<br>authentication process to verify that logical access<br>is implemented in accordance with all elements<br>specified in this requirement.|Disk-level encryption typically encrypts the entire disk<br>or partition using the same key, with all data<br>automatically decrypted when the system runs or when<br>an authorized user requests it. Many disk-encryption<br>solutions intercept operating system read/write<br>operations and perform the appropriate cryptographic<br>transformations without any special action by the user|
|authentication and access control mechanisms.<br>•<br>Decryption keys are not associated with user<br>accounts.<br>•<br>Authentication factors (passwords, passphrases, or<br>cryptographic keys) that allow access to<br>unencrypted data are stored securely.|**3.5.1.3.b**Examine files containing authentication<br>factors (passwords, passphrases, or cryptographic<br>keys) and interview personnel to verify that<br>authentication factors that allow access to<br>unencrypted data are stored securely and are<br>independent from the native operating system’s<br>authentication and access control methods.|other than supplying a password or passphrase at<br>system start-up or at the beginning of a session. This<br>provides no protection from a malicious individual that<br>has already managed to gain access to a valid user<br>account.<br>**Good Practice**<br>Full disk encryption helps to protect data in the event of|
|**Customized Approach Objective**||physical loss of a disk and therefore its use is best<br>limited only to removable electronic media storage|
|Disk encryption implementations are configured to||devices.|



**Customized Approach Objective** Disk encryption implementations are configured to require independent authentication and logical access controls for decryption. **Applicability Notes** Disk or partition encryption implementations must also meet all other PCI DSS encryption and key-management requirements. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 95_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **3.6 Cryptographic keys used to protect stored account data are secured.** 

**Defined Approach Requirements Defined Approach Testing Procedures 3.6.1** Procedures are defined and implemented to **3.6.1** Examine documented key-management protect cryptographic keys used to protect stored policies and procedures to verify that processes to account data against disclosure and misuse that protect cryptographic keys used to protect stored include: account data against disclosure and misuse are • Access to keys is restricted to the fewest defined to include all elements specified in this number of custodians necessary. requirement. 

- Access to keys is restricted to the fewest number of custodians necessary. 

- Key-encrypting keys are at least as strong as the data-encrypting keys they protect. 

- Key-encrypting keys are stored separately from data-encrypting keys. 

- Keys are stored securely in the fewest possible locations and forms. 

###### **Customized Approach Objective** 

Processes that protect cryptographic keys used to protect stored account data against disclosure and misuse are defined and implemented. 

###### **Purpose** 

Cryptographic keys must be strongly protected because those who obtain access will be able to decrypt data. **Good Practice** 

Having a centralized key management system based on industry standards is recommended for managing cryptographic keys. 

###### **Further Information** 

The entity’s key management procedures will benefit through alignment with industry requirements, Sources for information on cryptographic key management life cycles include: 

- _ISO 11568-1 Banking — Key management (retail) — Part 1_ : Principles (specifically Chapter 10 and the referenced Parts 2 & 4) 

- _NIST SP 800-57 Part 1 Revision 5— Recommendation for Key Management, Part 1: General_ . 

###### **Applicability Notes** 

This requirement applies to keys used to protect stored account data and to key-encrypting keys used to protect data-encrypting keys. 

The requirement to protect keys used to protect stored account data from disclosure and misuse applies to both data-encrypting keys and keyencrypting keys. Because one key-encrypting key may grant access to many data-encrypting keys, the key-encrypting keys require strong protection measures. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 96_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.6.1.1** **_Additional requirement for service_**<br>**_providers only:_**A documented description of the<br>cryptographic architecture is maintained that<br>includes:<br>•<br>Details of all algorithms, protocols, and keys<br>used for the protection of stored account data,<br>including key strength and expiry date.<br>•<br>Preventing the use of the same cryptographic<br>keys in production and test environments._This_<br>_bullet is a best practice until its effective date;_<br>_refer to Applicability Notes below for details._|**3.6.1.1** **_Additional testing procedure for service_**<br>**_provider assessments only:_**Interview<br>responsible personnel and examine documentation<br>to verify that a document exists to describe the<br>cryptographic architecture that includes all<br>elements specified in this requirement.|Maintaining current documentation of the cryptographic<br>architecture enables an entity to understand the<br>algorithms, protocols, and cryptographic keys used to<br>protect stored account data, as well as the devices that<br>generate, use, and protect the keys. This allows an<br>entity to keep pace with evolving threats to its<br>architecture and plan for updates as the assurance<br>level provided by different algorithms and key strengths<br>changes. Maintaining such documentation also allows<br>an entity to detect lost or missing keys or key-<br>management devices and identify unauthorized<br>additions to its cryptographic architecture.|
|•<br>Description of the key usage for each key.<br>•<br>Inventory of any hardware security modules<br>(HSMs), key management systems (KMS), and<br>other secure cryptographic devices (SCDs) used<br>for key management, including type and location||The use of the same cryptographic keys in both<br>production and test environments introduces a risk of<br>exposing the key if the test environment is not at the<br>same security level as the production environment.<br>**Good Practice**|
|of devices, to support meeting Requirement<br>12.3.4.||Having an automated reporting mechanism can assist<br>with maintenance of the cryptographic attributes.|



|**Customized Approach Objective**|
|---|
|Accurate details of the cryptographic architecture|
|are maintained and available.|
|_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 97_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Applicability Notes**||
|This requirement applies only when the entity being<br>assessed is a service provider.||
|In cloud HSM implementations, responsibility for the<br>cryptographic architecture according to this<br>Requirement will be shared between the cloud<br>provider and the cloud customer.||
|_The bullet above (for including, in the cryptographic_<br>_architecture, that the use of the same cryptographic_<br>_keys in production and test is prevented) is a best_<br>_practice until 31 March 2025, after which it will be_<br>_required as part of Requirement 3.6.1.1 and must_<br>_be fully considered during a PCI DSS assessment._||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 98_ 



###### **Requirements and Testing Procedures** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|
|---|---|
|**3.6.1.2**Secret and private keys used to protect<br>stored account data are stored in one (or more) of<br>the following forms at all times:<br>•<br>Encrypted with a key-encrypting key that is at<br>least as strong as the data-encrypting key, and|**3.6.1.2.a**Examine documented procedures to<br>verify it is defined that cryptographic keys used to<br>encrypt/decrypt stored account data must exist<br>only in one (or more) of the forms specified in this<br>requirement.|
|that is stored separately from the data-<br>encrypting key.<br>•<br>Within a secure cryptographic device (SCD),<br>such as a hardware security module (HSM) or<br>PTS-approved point-of-interaction device.<br>•<br>As at least two full-length key components or|**3.6.1.2.b**Examine system configurations and key<br>storage locations to verify that cryptographic keys<br>used to encrypt/decrypt stored account data exist<br>in one (or more) of the forms specified in this<br>requirement.|
|key shares, in accordance with an industry-<br>accepted method.<br>**Customized Approach Objective**<br>Secret and private keys are stored in a secure form<br>that prevents unauthorized retrieval or access.|**3.6.1.2.c**Wherever key-encrypting keys are used,<br>examine system configurations and key storage<br>locations to verify:<br>•<br>Key-encrypting keys are at least as strong as<br>the data-encrypting keys they protect.<br>•<br>Key-encrypting keys are stored separately from<br>data-encrypting keys.|
|_(continued on next page)_||



###### **Guidance** 

**Purpose** Storing cryptographic keys securely prevents unauthorized or unnecessary access that could result in the exposure of stored account data. Storing keys separately means they are stored such that if the location of one key is compromised, the second key is not also compromised. **Good Practice** Where data-encrypting keys are stored in an HSM, the HSM interaction channel should be protected to prevent interception of encryption or decryption operations. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 99_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Applicability Notes**|
|---|
|It is not required that public keys be stored in one of<br>these forms.|
|Cryptographic keys stored as part of a key<br>management system (KMS) that employs SCDs are<br>acceptable.|
|A cryptographic key that is split into two parts does<br>not meet this requirement. Secret or private keys<br>stored as key components or key shares must be<br>generated via one of the following:<br>•<br>Using an approved random number generator<br>and within an SCD,<br>**OR**|
|•<br>According to ISO 19592 or equivalent industry<br>standard for generation of secret key shares.|



|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**3.6.1.3**Access to cleartext cryptographic key<br>components is restricted to the fewest number of<br>custodians necessary.|**3.6.1.3**Examine user access lists to verify that<br>access to cleartext cryptographic key components<br>is restricted to the fewest number of custodians<br>necessar|Restricting the number of people who have access to<br>cleartext cryptographic key components reduces the<br>risk of stored account data being retrieved or rendered<br>visible by unauthorized parties.|
|**Customized Approach Objective**|y.|**Good Practice**<br>Only personnel with defined key custodian|
|Access to cleartext cryptographic key components<br>is restricted to necessary personnel.||responsibilities (creating, altering, rotating, distributing,<br>or otherwise maintaining encryption keys) should be<br>granted access to key components.<br>Ideally this will be a very small number of people.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 100_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.6.1.4**Cryptographic keys are stored in the fewest<br>possible locations.<br>**Customized Approach Objective**|**3.6.1.4**Examine key storage locations and observe<br>processes to verify that keys are stored in the<br>fewest possible locations.|Storing any cryptographic keys in the fewest locations<br>helps an organization track and monitor all key<br>locations and minimizes the potential for keys to be<br>exposed to unauthorized parties.|
|Cryptographic keys are retained only where<br>necessary.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 101_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**3.7 Where cryptography is used to protect store**<br>**lifecycle are defined and implemented.**<br>**Defined Approach Requirements**|**d account data, key management processes an**<br>**Defined Approach Testing Procedures**|**d procedures covering all aspects of the key**<br>**Purpose**|
|**3.7.1**Key-management policies and procedures are<br>implemented to include generation of strong<br>cryptographic keys used to protect stored account<br>data.<br>**Customized Approach Objective**|**3.7.1.a**Examine the documented key-management<br>policies and procedures for keys used for<br>protection of stored account data to verify that they<br>define generation of strong cryptographic keys.<br>**3.7.1.b**Observe the method for generating keys to<br>verify that strong keys are generated.|Use of strong cryptographic keys significantly increases<br>the level of security of encrypted account data.<br>**Further Information**<br>See the sources referenced at Cryptographic Key<br>Generation in_Appendix G_.|
|Strong cryptographic keys are generated.|||
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.7.2**Key-management policies and procedures are<br>implemented to include secure distribution of<br>cryptographic keys used to protect stored account<br>data.|**3.7.2.a**Examine the documented key-management<br>policies and procedures for keys used for<br>protection of stored account data to verify that they<br>define secure distribution of cryptographic keys.|Secure distribution or conveyance of secret or private<br>cryptographic keys means that keys are distributed only<br>to authorized custodians, as identified in Requirement<br>3.6.1.2, and are never distributed insecurely.|
|**Customized Approach Objective**|**3.7.2.b**Observe the method for distributing keys to<br>verify that keys are distributed securely.||
|Cryptographic keys are secured during distribution.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 102_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.7.3**Key-management policies and procedures are<br>implemented to include secure storage of<br>cryptographic keys used to protect stored account<br>data.<br>**Customized Approach Objective**<br>Cryptographic keys are secured when stored.|**3.7.3.a**Examine the documented key-management<br>policies and procedures for keys used for<br>protection of stored account data to verify that they<br>define secure storage of cryptographic keys.<br>**3.7.3.b**Observe the method for storing keys to<br>verify that keys are stored securely.|Storing keys without proper protection could provide<br>access to attackers, resulting in the decryption and<br>exposure of account data.<br>**Good Practice**<br>Data encryption keys can be protected by encrypting<br>them with a key-encrypting key.<br>Keys can be stored in a Hardware Security Module<br>(HSM).<br>Secret or private keys that can decrypt data should<br>never be present in source code.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 103_ 



###### **Requirements and Testing Procedures** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|
|---|---|
|**3.7.4**Key management policies and procedures are<br>implemented for cryptographic key changes for keys<br>that have reached the end of their cryptoperiod, as<br>defined by the associated application vendor or key<br>owner, and based on industry best practices and<br>guidelines, including the following:|**3.7.4.a**Examine the documented key-management<br>policies and procedures for keys used for<br>protection of stored account data to verify that they<br>define changes to cryptographic keys that have<br>reached the end of their cryptoperiod and include<br>all elements specified in this requirement.|
|•<br>A defined cryptoperiod for each key type in use.<br>•<br>A process for key changes at the end of the<br>defined cryptoperiod.<br>**Customized Approach Objective**|**3.7.4.b**Interview personnel, examine<br>documentation, and observe key storage locations<br>to verify that keys are changed at the end of the<br>defined cryptoperiod(s).|
|Cryptographic keys are not used beyond their<br>defined cryptoperiod.||



###### **Guidance** 

###### **Purpose** 

Changing encryption keys when they reach the end of their cryptoperiod is imperative to minimize the risk of someone obtaining the encryption keys and using them to decrypt data. 

###### **Definitions** 

A cryptoperiod is the time span during which a cryptographic key can be used for its defined purpose. Cryptoperiods are often defined in terms of the period for which the key is active and/or the amount of ciphertext that has been produced by the key. Considerations for defining the cryptoperiod include, but are not limited to, the strength of the underlying algorithm, size or length of the key, risk of key compromise, and the sensitivity of the data being encrypted. 

###### **Further Information** 

_NIST SP 800-57 Part 1, Revision 5, Section 5.3 Cryptoperiods_ – provides guidance for establishing the time span during which a specific key is authorized for use by legitimate entities, or the keys for a given system will remain in effect. See Table 1 of _SP 800-57_ Part 1 for suggested cryptoperiods for different key types. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 104_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.7.5**Key management policies procedures are<br>implemented to include the retirement, replacement,<br>or destruction of keys used to protect stored<br>account data, as deemed necessary when:<br>•<br>The key has reached the end of its defined<br>cryptoperiod.|**3.7.5.a**Examine the documented key-management<br>policies and procedures for keys used for<br>protection of stored account data and verify that<br>they define retirement, replacement, or destruction<br>of keys in accordance with all elements specified in<br>this requirement.|Keys that are no longer required, keys with weakened<br>integrity, and keys that are known or suspected to be<br>compromised, should be archived, revoked, and/or<br>destroyed to ensure that the keys can no longer be<br>used.<br>If such keys need to be kept (for example, to support<br>archived encrypted data), they should be strongly|
|•<br>The integrity of the key has been weakened,<br>including when personnel with knowledge of a<br>cleartext key component leaves the company, or<br>the role for which the key component was<br>known.<br>•<br>The key is suspected of or known to be<br>compromised.<br>Retired or replaced keys are not used for encryption<br>operations.|**3.7.5.b**Interview personnel to verify that processes<br>are implemented in accordance with all elements<br>specified in this requirement.|protected.<br>**Good Practice**<br>Archived cryptographic keys should be used only for<br>decryption/verification purposes.<br>The encryption solution should provide for and facilitate<br>a process to replace keys that are due for replacement<br>or that are known to be, or suspected of being,<br>compromised. In addition, any keys that are known to<br>be, or suspected of being, compromised should be|
|**Customized Approach Objective**||managed in accordance with the entity’s incident<br>response plan per Requirement 12.10.1.|
|Keys are removed from active use when it is<br>suspected or known that the integrity of the key is<br>weakened.||**Further Information**<br>Industry best practices for archiving retired keys are<br>outlined in_NIST SP 800-57 Part 1, Revision 5, Section_<br>_8.3.1_, and includes maintaining the archive with a|
|**Applicability Notes**<br>If retired or replaced cryptographic keys need to be<br>retained, these keys must be securely archived (for<br>example, by using a key-encryption key).||trusted third party and storing archived key information<br>separately from operational data.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 105_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.7.6**Where manual cleartext cryptographic key-<br>management operations are performed by<br>personnel, key-management policies and<br>procedures are implemented, including managing<br>these operations using split knowledge and dual|**3.7.6.a**Examine the documented key-management<br>policies and procedures for keys used for<br>protection of stored account data and verify that<br>they define using split knowledge and dual control.|Split knowledge and dual control of keys are used to<br>eliminate the possibility of a single person having<br>access to the whole key and therefore being able to<br>gain unauthorized access to the data.<br>**Definitions**|
|<br>control.|**3.7.6.b**Interview personnel and/or observe<br>processes to verify that manual cleartext keys are|Split knowledge is a method in which two or more<br>people separately have key components, where each|
|**Customized Approach Objective**|<br>managed with split knowledge and dual control.|person knows only their own key component, and the<br>individual key components convey no knowledge of|
|Cleartext secret or private keys cannot be known by<br>anyone. Operations involving cleartext keys cannot<br>be carried out by a single person.<br>**Applicability Notes**||other components or of the original cryptographic key.<br>Dual control requires two or more people to<br>authenticate the use of a cryptographic key or perform<br>a key-management function. No single person can<br>access or use the authentication factor (for example,<br>the password, PIN, or key) of another.|
|This control is applicable for manual key-<br>management operations.||**Good Practice**<br>Where key components or key shares are used,|
|A cryptographic key that is simply split into two parts<br>does not meet this requirement. Secret or private<br>keys stored as key components or key shares must<br>be generated via one of the following:||<br>procedures should ensure that no single custodian ever<br>has access to sufficient key components or shares to<br>reconstruct the cryptographic key. For example, in an<br>m-of-n scheme (for example, Shamir), where only two|
|•Using an approved random number generator<br>and within a secure cryptographic device (SCD),<br>such as a hardware security module (HSM) or<br>PTS-approved point-of-interaction device,<br>**OR**<br>•According to ISO 19592 or equivalent industry<br>standard for generation of secret key shares.||of any three components are required to reconstruct the<br>cryptographic key, a custodian must not have current or<br>prior knowledge of more than one component. If a<br>custodian was previously assigned component A, which<br>was then reassigned, the custodian should not then be<br>assigned component B or C, as this would give the<br>custodian knowledge of two components and the ability<br>to recreate the key.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 106_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**3.7.6**_(continued)_||**Examples**<br>Key-management operations that might be performed<br>manually include, but are not limited to, key generation,<br>transmission, loading, storage, and destruction.<br>**Further Information**<br>Industry standards for managing key components<br>include:<br>•<br>_NIST SP 800-57_Part 2, Revision 1 --<br>Recommendation for Key Management: Part 2 –<br>Best Practices for Key Management Organizations<br>[4.6 Keying Material Distribution]<br>•<br>_ISO 11568-2 Banking — Key management (retail)_<br>_— Part 2_: Symmetric ciphers, their key<br>management and life cycle [4.7.2.3 Key<br>components and 4.9.3 Key components]<br>•<br>_European Payments Council EPC342-08_<br>_Guidelines on Cryptographic Algorithms Usage and_<br>_Key Management_[especially 4.1.4 Key installation].|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.7.7**Key management policies and procedures are<br>implemented to include the prevention of<br>unauthorized substitution of cryptographic keys.|**3.7.7.a**Examine the documented key-management<br>policies and procedures for keys used for<br>protection of stored account data and verify that<br>they define prevention of unauthorized substitution|If an attacker is able to substitute an entity’s key with a<br>key the attacker knows, the attacker will be able to<br>decrypt all data encrypted with that key.<br>**Good Practice**|
|**Customized Approach Objective**<br>Cryptographic keys cannot be substituted by<br>unauthorized personnel.|<br>of cryptographic keys.<br>**3.7.7.b**Interview personnel and/or observe<br>processes to verify that unauthorized substitution<br>of keys is prevented.|The encryption solution should not allow for or accept<br>substitution of keys from unauthorized sources or<br>unexpected processes.<br>Controls should include ensuring that individuals with<br>access to key components or shares do not have<br>access to other components or shares that form the<br>necessary threshold to derive the key.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 107_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**3.7.8**Key management policies and procedures are<br>implemented to include that cryptographic key<br>custodians formally acknowledge (in writing or<br>electronically) that they understand and accept their<br>key-custodian responsibilities.|**3.7.8.a**Examine the documented key-management<br>policies and procedures for keys used for<br>protection of stored account data and verify that<br>they define acknowledgments for key custodians in<br>accordance with all elements specified in this<br>requirement.<br>**3.7.8.b**Examine documentation or other evidence<br>showing that key custodians have provided|This process will help ensure individuals that act as key<br>custodians commit to the key-custodian role and<br>understand and accept the responsibilities. An annual<br>reaffirmation can help remind key custodians of their<br>responsibilities.<br>**Further Information**<br>Industry guidance for key custodians and their roles<br>and responsibilities includes:<br>•<br>_NIST SP 800-130 A Framework for Designing_|
|**Customized Approach Objective**<br>Key custodians are knowledgeable about their<br>responsibilities in relation to cryptographic<br>operations and can access assistance and guidance<br>when required.|acknowledgments in accordance with all elements<br>specified in this requirement.|_Cryptographic Key Management Systems_[5. Roles<br>and Responsibilities (especially) for Key<br>Custodians]<br>•<br>_ISO 11568-1 Banking -- Key management (retail) --_<br>_Part 1_: Principles [5 Principles of key management<br>(especially b)]|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 108_ 



###### **Requirements and Testing Procedures** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|
|---|---|
|**3.7.9** **_Additional requirement for service_**<br>**_providers only:_**Where a service provider shares<br>cryptographic keys with its customers for<br>transmission or storage of account data, guidance<br>on secure transmission, storage and updating of<br>such keys is documented and distributed to the<br>service provider’s customers.|**3.7.9** **_Additional testing procedure for service_**<br>**_provider assessments only:_**If the service<br>provider shares cryptographic keys with its<br>customers for transmission or storage of account<br>data, examine the documentation that the service<br>provider provides to its customers to verify it<br>includes guidance on how to securely transmit,<br>store, and update customers’ keys in accordance|
|**Customized Approach Objective**<br>Customers are provided with appropriate key<br>management guidance whenever they receive<br>shared cryptographic keys.|with all elements specified in Requirements 3.7.1<br>through 3.7.8 above.|
|**Applicability Notes**||
|This requirement applies only when the entity being<br>assessed is a service provider.||



###### **Guidance** 

###### **Purpose** 

Providing guidance to customers on how to securely transmit, store, and update cryptographic keys can help prevent keys from being mismanaged or disclosed to unauthorized entities. 

###### **Further Information** 

Numerous industry standards for key management are cited above in the Guidance for Requirements 3.7.13.7.8. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 109_ 



#### **_Requirement 4: Protect Cardholder Data with Strong Cryptography During Transmission Over Open, Public Networks_** 

**Sections** 

- **4.1** Processes and mechanisms for protecting cardholder data with strong cryptography during transmission over open, public networks are defined and understood. 

- **4.2** PAN is protected with strong cryptography during transmission 

###### **Overview** 

The use of strong cryptography provides greater assurance in preserving data confidentiality, integrity, and non-repudiation. 

To protect against compromise, PAN must be encrypted during transmission over networks that are easily accessed by malicious individuals, including untrusted and public networks. Misconfigured wireless networks and vulnerabilities in legacy encryption and authentication protocols continue to be targeted by malicious individuals aiming to exploit these vulnerabilities to gain privileged access to cardholder data environments (CDE). Any transmissions of cardholder data over an entity’s internal network(s) will naturally bring that network into scope for PCI DSS since that network stores, processes, or transmits cardholder data. Any such networks must be evaluated and assessed against applicable PCI DSS requirements. 

Requirement 4 applies to transmissions of PAN unless specifically called out in an individual requirement. 

PAN transmissions can be protected by encrypting the data before it is transmitted, or by encrypting the session over which the data is transmitted, or both. While it is not required that strong cryptography be applied at both the data level and the session level, it is recommended. Refer to _Appendix G_ for definitions of “strong cryptography” and other PCI DSS terms. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 110_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**4.1 Processes and mechanisms for protecting**<br>**defined and understood.**|**cardholder data with strong cryptography during**|**transmission over open, public networks are**|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**4.1.1**All security policies and operational<br>procedures that are identified in Requirement 4 are:<br>•<br>Documented.<br>•<br>Kept up to date.<br>•<br>In use.<br>•<br>Known to all affected parties.|**4.1.1**Examine documentation and interview<br>personnel to verify that security policies and<br>operational procedures identified in Requirement 4<br>are managed in accordance with all elements<br>specified in this requirement.|Requirement 4.1.1 is about effectively managing<br>and maintaining the various policies and<br>procedures specified throughout Requirement 4.<br>While it is important to define the specific policies<br>or procedures called out in Requirement 4, it is<br>equally important to ensure they are properly<br>documented, maintained, and disseminated.<br>**Good Practice**|
|**Customized Approach Objective**||It is important to update policies and procedures<br>as needed to address changes in processes,|
|Expectations, controls, and oversight for meeting<br>activities within Requirement 4 are defined and<br>adhered to by affected personnel. All supporting<br>activities are repeatable, consistently applied, and<br>conform to management’s intent.||technologies, and business objectives. For this<br>reason, consider updating these documents as<br>soon as possible after a change occurs and not<br>only on a periodic cycle.<br>**Definitions**<br>Security policies define the entity’s security<br>objectives and principles. Operational procedures<br>describe how to perform activities, and define the<br>controls, methods, and processes that are<br>followed to achieve the desired result in a<br>consistent manner and in accordance with policy<br>objectives. Policies and procedures, including<br>updates, are actively communicated to all affected<br>personnel, and are supported by operating<br>procedures describing how to perform activities.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 111_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**4.1.2**Roles and responsibilities for performing<br>activities in Requirement 4 are documented,<br>assigned, and understood.|**4.1.2.a**Examine documentation to verify that<br>descriptions of roles and responsibilities for<br>performing activities in Requirement 4 are<br>documented and assigned.|If roles and responsibilities are not formally<br>assigned, personnel may not be aware of their<br>day-to-day responsibilities and critical activities<br>may not occur.<br>**Good Practice**|
|**Customized Approach Objective**|**4.1.2.b**Interview personnel with responsibility for<br>performing activities in Requirement 4 to verify that<br>roles and responsibilities are assigned as<br>documented and are understood.|Roles and responsibilities may be documented<br>within policies and procedures or maintained<br>within separate documents.<br>As part of communicating roles and<br>responsibilities, entities can consider having<br>personnel acknowledge their acceptance and<br>understanding of their assigned roles and<br>responsibilities.|
|Day-to-day responsibilities for performing all the<br>activities in Requirement 4 are allocated. Personnel<br>are accountable for successful, continuous<br>operation of these requirements.||**Examples**<br>A method to document roles and responsibilities<br>is a responsibility assignment matrix that includes<br>who is responsible, accountable, consulted, and<br>informed (also called a RACI matrix).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 112_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**4.2 PAN is protected with strong cryptography**|**during transmission.**||
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**4.2.1**Strong cryptography and security protocols<br>are implemented as follows to safeguard PAN<br>during transmission over open, public networks:<br>•<br>Only trusted keys and certificates are accepted.|**4.2.1.a**Examine documented policies and<br>procedures and interview personnel to verify<br>processes are defined to include all elements<br>specified in this requirement.|Sensitive information must be encrypted during<br>transmission over public networks because it is<br>easy and common for a malicious individual to<br>intercept and/or divert data while in transit.<br>**Good Practice**|
|•<br>Certificates used to safeguard PAN during<br>transmission over open, public networks are<br>confirmed as valid and are not expired or<br>revoked._This bullet is a best practice until its_<br>_effective date; refer to applicability notes below_<br>|**4.2.1.b**Examine system configurations to verify<br>that strong cryptography and security protocols are<br>implemented in accordance with all elements<br>specified in this requirement.|The network and data-flow diagrams defined in<br>Requirement 1 are useful resources for identifying<br>all connection points where account data is<br>transmitted or received over open, public<br>networks.|
|_for details._<br>•<br>The protocol in use supports only secure<br>versions or configurations and does not support<br>fallback to, or use of insecure versions,<br>algorithms, key sizes, or implementations.|**4.2.1.c**Examine cardholder data transmissions to<br>verify that all PAN is encrypted with strong<br>cryptography when it is transmitted over open,<br>public networks.|While not required, it is considered a good<br>practice for entities to also encrypt PAN over their<br>internal networks, and for entities to establish any<br>new network implementations with encrypted<br>communications.|
|•<br>The encryption strength is appropriate for the<br>encryption methodology in use.<br>**Customized Approach Objective**|**4.2.1.d**Examine system configurations to verify<br>that keys and/or certificates that cannot be verified<br>as trusted are rejected.|PAN transmissions can be protected by<br>encrypting the data before it is transmitted, or by<br>encrypting the session over which the data is<br>transmitted, or both. While it is not required that|
|Cleartext PAN cannot be read or intercepted from<br>any transmissions over open, public networks.||strong cryptography be applied at both the data<br>level and the session level, it is strongly<br>recommended. If encrypted at the data level, the<br>cryptographic keys used for protecting the data<br>can be managed in accordance with<br>Requirements 3.6 and 3.7. If the data is encrypted<br>at the session level, designated key custodians<br>should be assigned responsibility for managing<br>transmission keys and certificates.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 113_ 



###### **Requirements and Testing Procedures Guidance** 

|**Applicability Notes**|Some protocol implementations (such as SSL,<br>SSH v1.0, and early TLS) have known|
|---|---|
|A self-signed certificate may also be acceptable if<br>the certificate is issued by an internal CA within the<br>organization, the certificate’s author is confirmed,<br>and the certificate is verified—for example, via hash<br>or signature—and has not expired.|vulnerabilities that an attacker can use to gain<br>access to the cleartext data. It is critical that<br>entities maintain awareness of industry-defined<br>deprecation dates for the cipher suites they are<br>using and are prepared to migrate to newer|
|_The bullet above (for confirming that certificates_<br>_used to safeguard PAN during transmission over_|versions or protocols when older ones are no<br>longer deemed secure.|
|_open, public networks are valid and are not expired_<br>_or revoked) is a best practice until 31 March 2025,_<br>_after which it will be required as part of Requirement_<br>_4.2.1 and must be fully considered during a PCI_<br>_DSS assessment._|Verifying that certificates are trusted helps ensure<br>the integrity of the secure connection. To be<br>considered trusted, a certificate should be issued<br>from a trusted source, such as a trusted certificate<br>authority (CA), and not be expired. Up-to-date<br>Certificate Revocation Lists (CRLs) or Online<br>Certificate Status Protocol (OCSP) can be used to<br>validate certificates.<br>Techniques to validate certificates may include<br>certificate and public key pinning, where the<br>trusted certificate or a public key is pinned either<br>during development or upon its first use. Entities<br>can also confirm with developers or review source<br>code to ensure that clients and servers reject<br>connections if the certificate is bad.<br>For browser-based TLS certificates, certificate<br>trust can often be verified by clicking on the lock<br>icon that appears next to the address bar.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 114_ 



||**Requirements and Testing Procedures**|**Guidance**|
|---|---|---|
|**4.2.1**_(continued)_||**Examples**<br>Open, public networks include, but are not limited<br>to:<br>•<br>The Internet and<br>•<br>Wireless technologies, including Wi-Fi,<br>Bluetooth, cellular technologies, and satellite<br>communications.<br>**Further Information**<br>Vendor recommendations and industry best<br>practices can be consulted for information about<br>the proper encryption strength specific to the<br>encryption methodology in use.<br>For more information about strong cryptography<br>and secure protocols, see industry standards and<br>best practices such as_NIST SP 800-52_and_SP_<br>_800-57_.<br>For more information about trusted keys and<br>certificates, see_NIST_ _Cybersecurity Practice_<br>_Guide Special Publication 1800-16_,_Securing Web_<br>_Transactions: Transport Layer Security (TLS)_<br>_Server Certificate Management._|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 115_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**4.2.1.1**An inventory of the entity’s trusted keys and<br>certificates used to protect PAN during transmission<br>is maintained.|**4.2.1.1.a**Examine documented policies and<br>procedures to verify processes are defined for the<br>entity to maintain an inventory of its trusted keys<br>and certificates.|The inventory of trusted keys helps the entity<br>keep track of the algorithms, protocols, key<br>strength, key custodians, and key expiry dates.<br>This enables the entity to respond quickly to<br>vulnerabilities discovered in encryption software,<br>|
||**4.2.1.1.b**Examine the inventory of trusted keys<br>and certificates to verify it is kept up to date.|certificates, and cryptographic algorithms.<br>**Good Practice**|
|**Customized Approach Objective**||For certificates, the inventory should include the<br>issuing CA and certification expiration date.|
|All keys and certificates used to protect PAN during<br>transmission are identified and confirmed as trusted.|||
|**Applicability Notes**|||
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 116_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**4.2.1.2**Wireless networks transmitting PAN or<br>connected to the CDE use industry best practices to<br>implement strong cryptography for authentication<br>and transmission.<br>**Customized Approach Objective**|**4.2.1.2**Examine system configurations to verify<br>that wireless networks transmitting PAN or<br>connected to the CDE use industry best practices<br>to implement strong cryptography for<br>authentication and transmission.|Since wireless networks do not require physical<br>media to connect, it is important to establish<br>controls limiting who can connect and what<br>transmission protocols will be used. Malicious<br>users use free and widely available tools to<br>eavesdrop on wireless communications. Use of<br>strong cryptography can help limit disclosure of|
|Cleartext PAN cannot be read or intercepted from<br>wireless network transmissions.||sensitive information across wireless networks.<br>Wireless networks present unique risks to an<br>organization; therefore, they must be identified<br>and protected according to industry requirements.<br>Strong cryptography for authentication and<br>transmission of PAN is required to prevent<br>malicious users from gaining access to the<br>wireless network or utilizing wireless networks to<br>access other internal networks or data.<br>**Good Practice**|
|||Wireless networks should not permit fallback or<br>downgrade to an insecure protocol or lower<br>encryption strength that does not meet the intent<br>of strong cryptography.<br>**Further Information**<br>Review the vendor’s specific documentation for<br>more details on the choice of protocols,<br>configurations, and settings related to<br>cryptography.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 117_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**4.2.2**PAN is secured with strong cryptography<br>whenever it is sent via end-user messaging<br>technologies.|**4.2.2.a**Examine documented policies and<br>procedures to verify that processes are defined to<br>secure PAN with strong cryptography whenever<br>sent over end-user messaging technologies.|End-user messaging technologies typically can be<br>easily intercepted by packet-sniffing during<br>delivery across internal and public networks.<br>**Good Practice**<br>The use of end-user messaging technology to|
||**4.2.2.b**Examine system configurations and vendor<br>documentation to verify that PAN is secured with|send PAN should only be considered where there<br>is a defined business need and should be|
|**Customized Approach Objective**<br>Cleartext PAN cannot be read or intercepted from<br>transmissions using end-user messaging<br>technologies.|<br>strong cryptography whenever it is sent via end-<br>user messaging technologies.|controlled through the Acceptable Use Policies for<br>end-user technologies defined by the entity<br>according to Requirement 12.2.1.<br>**Examples**<br>E-mail, instant messaging, SMS, and chat are|
|**Applicability Notes**||examples of the type of end-user messaging<br>technology that this requirement refers to.|
|This requirement also applies if a customer, or other<br>third party, requests that PAN is sent to them via<br>end-user messaging technologies.<br>There could be occurrences where an entity<br>receives unsolicited cardholder data via an insecure<br>communication channel that was not intended for<br>transmissions of sensitive data. In this situation, the<br>entity can choose to either include the channel in<br>the scope of their CDE and secure it according to<br>PCI DSS or delete the cardholder data and<br>implement measures to prevent the channel from<br>being used for cardholder data.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 118_ 



### **Maintain a Vulnerability Management Program** 

#### **_Requirement 5: Protect All Systems and Networks from Malicious Software_** 

###### **Sections** 

- **5.1** Processes and mechanisms for protecting all systems and networks from malicious software are defined and understood. 

- **5.2** Malicious software (malware) is prevented, or detected and addressed. 

- **5.3** Anti-malware mechanisms and processes are active, maintained, and monitored. 

- **5.4** Anti-phishing mechanisms protect users against phishing attacks. 

###### **Overview** 

Malicious software (malware) is software or firmware designed to infiltrate or damage a computer system without the owner's knowledge or consent, with the intent of compromising the confidentiality, integrity, or availability of the owner’s data, applications, or operating system. 

Examples include viruses, worms, Trojans, spyware, ransomware, keyloggers, rootkits, malicious code, scripts, and links. 

Malware can enter the network during many business-approved activities, including employee e-mail (for example, via phishing) and use of the Internet, mobile computers, and storage devices, resulting in the exploitation of system vulnerabilities. 

Using anti-malware solutions that address all types of malware helps to protect systems from current and evolving malware threats. Refer to _Appendix G_ for definitions of PCI DSS terms. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 119_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **5.1 Processes and mechanisms for protecting all systems and networks from malicious software are defined and understood.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**5.1.1**All security policies and operational<br>procedures that are identified in Requirement 5 are:<br>•<br>Documented.<br>•<br>Kept up to date.<br>•<br>In use.<br>•<br>Known to all affected parties.|**5.1.1**Examine documentation and interview<br>personnel to verify that security policies and<br>operational procedures identified in Requirement 5<br>are managed in accordance with all elements<br>specified in this requirement.|Requirement 5.1.1 is about effectively managing<br>and maintaining the various policies and procedures<br>specified throughout Requirement 5. While it is<br>important to define the specific policies or<br>procedures called out in Requirement 5, it is equally<br>important to ensure they are properly documented,<br>maintained, and disseminated.<br>**Good Practice**|
|**Customized Approach Objective**||It is important to update policies and procedures as<br>needed to address changes in processes,|
|Expectations, controls, and oversight for meeting<br>activities within Requirement 5 are defined and<br>adhered to by affected personnel. All supporting<br>activities are repeatable, consistently applied, and<br>conform to management’s intent.||technologies, and business objectives. For this<br>reason, consider updating these documents as soon<br>as possible after a change occurs and not only on a<br>periodic cycle.<br>**Definitions**<br>Security policies define the entity’s security<br>objectives and principles. Operational procedures<br>describe how to perform activities, and define the<br>controls, methods, and processes that are followed<br>to achieve the desired result in a consistent manner<br>and in accordance with policy objectives.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 120_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**5.1.2**Roles and responsibilities for performing<br>activities in Requirement 5 are documented,<br>assigned, and understood.|**5.1.2.a**Examine documentation to verify that<br>descriptions of roles and responsibilities for<br>performing activities in Requirement 5 are<br>documented and assigned.<br>**5.1.2.b**Interview personnel with responsibility for<br>performing activities in Requirement 5 to verify that|If roles and responsibilities are not formally<br>assigned, networks and systems may not be<br>properly protected from malware.<br>**Good Practice**<br>Roles and responsibilities may be documented<br>within policies and procedures or maintained within<br>separate documents.|
|**Customized Approach Objective**<br>Day-to-day responsibilities for performing all the<br>activities in Requirement 5 are allocated. Personnel<br>are accountable for successful, continuous<br>operation of these requirements.|roles and responsibilities are assigned as<br>documented and are understood.|As part of communicating roles and responsibilities,<br>entities can consider having personnel acknowledge<br>their acceptance and understanding of their<br>assigned roles and responsibilities.<br>**Examples**<br>A method to document roles and responsibilities is a<br>responsibility assignment matrix that includes who is<br>responsible, accountable, consulted, and informed<br>(also called a RACI matrix).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 121_ 



###### **Requirements and Testing Procedures Guidance** 

###### **5.2 Malicious software (malware) is prevented, or detected and addressed.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**5.2.1**An anti-malware solution(s) is deployed on all<br>system components, except for those system<br>components identified in periodic evaluations per<br>Requirement 5.2.3 that concludes the system<br>components are not at risk from malware.|**5.2.1.a**Examine system components to verify that<br>an anti-malware solution(s) is deployed on all<br>system components, except for those determined<br>to not be at risk from malware based on periodic<br>evaluations per Requirement 5.2.3.|There is a constant stream of attacks targeting<br>newly discovered vulnerabilities in systems<br>previously regarded as secure. Without an anti-<br>malware solution that is updated regularly, new<br>forms of malware can be used to attack systems,<br>disable a network, or compromise data.|
|**Customized Approach Objective**<br>Automated mechanisms are implemented to prevent<br>systems from becoming an attack vector for<br>malware.|**5.2.1.b**For any system components without an<br>anti-malware solution, examine the periodic<br>evaluations to verify the component was evaluated<br>and the evaluation concludes that the component<br>is not at risk from malware.|**Good Practice**<br>It is beneficial for entities to be aware of "zero-day"<br>attacks (those that exploit a previously unknown<br>vulnerability) and consider solutions that focus on<br>behavioral characteristics and will alert and react to<br>unexpected behavior.<br>**Definitions**<br>System components known to be affected by<br>malware have active malware exploits available in<br>the real world (not only theoretical exploits).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 122_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**5.2.2**The deployed anti-malware solution(s):<br>•<br>Detects all known types of malware.<br>•<br>Removes, blocks, or contains all known types of<br>malware.|**5.2.2**Examine vendor documentation and<br>configurations of the anti-malware solution(s) to<br>verify that the solution:<br>•<br>Detects all known types of malware.<br>•<br>Removes, blocks, or contains all known types<br>of malware.|It is important to protect against all types and forms<br>of malware to prevent unauthorized access.<br>**Good Practice**<br>Anti-malware solutions may include a combination<br>of network-based controls, host-based controls, and<br>endpoint security solutions. In addition to signature-<br>based tools, capabilities used by modern anti-|
|**Customized Approach Objective**||malware solutions include sandboxing, privilege<br>escalation controls, and machine learning.|
|Malware cannot execute or infect other system<br>components.||Solution techniques include preventing malware<br>from getting into the network and removing or<br>containing malware that does get into the network.<br>**Examples**<br>Types of malware include, but are not limited to,<br>viruses, Trojans, worms, spyware, ransomware,<br>keyloggers, rootkits, malicious code, scripts, and<br>links.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 123_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**5.2.3**Any system components that are not at risk for<br>malware are evaluated periodically to include the<br>following:|**5.2.3.a**Examine documented policies and<br>procedures to verify that a process is defined for<br>periodic evaluations of any system components<br>|Certain systems, at a given point in time, may not<br>currently be commonly targeted or affected by<br>malware. However, industry trends for malware can<br>change quickly, so it is important for organizations|
|•<br>A documented list of all system components not<br>at risk for malware.|that are not at risk for malware that includes all<br>elements specified in this requirement.|to be aware of new malware that might affect their<br>systems—for example, by monitoring vendor<br>|
|•<br>Identification and evaluation of evolving<br>malware threats for those system components.|**5.2.3.b**Interview personnel to verify that the<br>evaluations include all elements specified in this|security notices and anti-malware forums to<br>determine whether its systems might be coming<br>under threat from new and evolving malware.|
|•<br>Confirmation whether such system components<br>continue to not require anti-malware protection.|requirement.|<br>**Good Practice**|
||**5.2.3.c**Examine the list of system components<br>identified as not at risk of malware and compare to<br>the system components without an anti-malware<br>solution deployed per Requirement 5.2.1 to verify|If an entity determines that a particular system is not<br>susceptible to any malware, the determination<br>should be supported by industry evidence, vendor<br>resources, and best practices.|
|**Customized Approach Objective**|<br>that the system components match for both|The following steps can help entities during their|
|The entity maintains awareness of evolving malware<br>threats to ensure that any systems not protected<br>from malware are not at risk of infection.|requirements.|periodic evaluations:<br>•<br>Identification of all system types previously<br>determined to not require malware protection.<br>•<br>Review of industry vulnerability alerts and|
|**Applicability Notes**||notices to determine if new threats exist for any<br>identified system.|
|System components covered by this requirement<br>are those for which there is no anti-malware solution<br>deployed per Requirement 5.2.1.||•<br>A documented conclusion about whether the<br>system types remain not susceptible to malware.<br>•<br>A strategy to add malware protection for any<br>system types for which malware protection has<br>become necessary.<br>Trends in malware should be included in the<br>identification of new security vulnerabilities at<br>Requirement 6.3.1, and methods to address new<br>trends should be incorporated into the entity’s<br>configuration standards and protection mechanisms<br>as needed.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 124_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**5.2.3.1**The frequency of periodic evaluations of<br>system components identified as not at risk for<br>malware is defined in the entity’s targeted risk<br>analysis, which is performed according to all<br>elements specified in Requirement 12.3.1.|**5.2.3.1.a**Examine the entity’s targeted risk<br>analysis for the frequency of periodic evaluations<br>of system components identified as not at risk for<br>malware to verify the risk analysis was performed<br>in accordance with all elements specified in<br>Requirement 12.3.1.|Entities determine the optimum period to undertake<br>the evaluation based on criteria such as the<br>complexity of each entity’s environment and the<br>number of types of systems that are required to be<br>evaluated.|
||**5.2.3.1.b**Examine documented results of periodic<br>evaluations of system components identified as not||
|**Customized Approach Objective**|at risk for malware and interview personnel to<br>verify that evaluations are performed at the||
|Systems not known to be at risk from malware are<br>re-evaluated at a frequency that addresses the<br>entity’s risk.|frequency defined in the entity’s targeted risk<br>analysis performed for this requirement.||
|**Applicability Notes**|||
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 125_ 



###### **Requirements and Testing Procedures Guidance** 

|**5.3 Anti-malware mechanisms and processes a**|**re active, maintained, and monitored.**||
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**5.3.1**The anti-malware solution(s) is kept current<br>via automatic updates.|**5.3.1.a**Examine anti-malware solution(s)<br>configurations, including any master installation of<br>the software, to verify the solution is configured to<br>perform automatic updates.|For an anti-malware solution to remain effective, it<br>needs to have the latest security updates,<br>signatures, threat analysis engines, and any other<br>malware protections on which the solution relies.<br>Having an automated update process avoids|
||**5.3.1.b**Examine system components and logs, to<br>verify that the anti-malware solution(s) and|burdening end users with responsibility for manually<br>installing updates and provides greater assurance|
|**Customized Approach Objective**<br>Anti-malware mechanisms can detect and address<br>the latest malware threats.|<br>definitions are current and have been promptly<br>deployed|that anti-malware protection mechanisms are<br>updated as quickly as possible after an update is<br>released.<br>**Good Practice**<br>Anti-malware mechanisms should be updated via a<br>trusted source as soon as possible after an update<br>is available. Using a trusted common source to<br>distribute updates to end-user systems helps ensure<br>the integrity and consistency of the solution<br>architecture.<br>Updates may be automatically downloaded to a<br>central location—for example, to allow for testing—<br>prior to being deployed to individual system<br>components.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 126_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**5.3.2**The anti-malware solution(s):<br>•<br>Performs periodic scans and active or real-time<br>scans.<br>**OR**<br>•<br>Performs continuous behavioral analysis of|**5.3.2.a**Examine anti-malware solution(s)<br>configurations, including any master installation of<br>the software, to verify the solution(s) is configured<br>to perform at least one of the elements specified in<br>this requirement.|Periodic scans can identify malware that is present,<br>but currently inactive, within the environment. Some<br>malware, such as zero-day malware, can enter an<br>environment before the scan solution is capable of<br>detecting it. Performing regular periodic scans or<br>continuous behavioral analysis of systems or<br>|
|<br>systems or processes.|**5.3.2.b**Examine system components, including all<br>operating system types identified as at risk for<br>malware, to verify the solution(s) is enabled in<br>accordance with at least one of the elements<br>specified in this requirement.|processes helps ensure that previously<br>undetectable malware can be identified, removed,<br>and investigated to determine how it gained access<br>to the environment.<br>**Good Practice**<br>Using a combination of periodic scans (scheduled|
|**Customized Approach Objective**<br>Malware cannot complete execution.|**5.3.2.c**Examine logs and scan results to verify that<br>the solution(s) is enabled in accordance with at<br>least one of the elements specified in this<br>requirement.|and on-demand) and active, real-time (on-access)<br>scanning helps ensure that malware residing in both<br>static and dynamic elements of the CDE is<br>addressed. Users should also be able to run on-<br>demand scans on their systems if suspicious activity<br>is detected – this can be useful in the early<br>detection of malware.<br>Scans should include the entire file system,<br>including all disks, memory, and start-up files and<br>boot records (at system restart) to detect all<br>malware upon file execution, including any software<br>that may be resident on a system but not currently<br>active. Scan scope should include all systems and<br>software in the CDE, including those that are often<br>overlooked such as email servers, web browsers,<br>and instant messaging software.<br>**Definitions**<br>Active, or real-time, scanning checks files for<br>malware upon any attempt to open, close, rename,<br>or otherwise interact with a file, preventing the<br>malware from being activated.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 127_ 



|**Requirements and**|**Testing Procedures**||**Guidance**|
|---|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**||
|**5.3.2.1**If periodic malware scans are performed to<br>meet Requirement 5.3.2, the frequency of scans is<br>defined in the entity’s targeted risk analysis, which<br>is performed according to all elements specified in<br>Requirement 12.3.1.|**5.3.2.1.a**Examine the entity’s targeted risk<br>analysis for the frequency of periodic malware<br>scans to verify the risk analysis was performed in<br>accordance with all elements specified in<br>Requirement 12.3.1.|Entities can dete<br>undertake period<br>assessment of th<br>environments.|rmine the optimum period to<br>ic scans based on their own<br>e risks posed to their|
||**5.3.2.1.b**Examine documented results of periodic<br>malware scans and interview personnel to verify<br>scans are performed at the frequency defined in<br>the entity’s targeted risk analysis performed for this<br>|||
|**Customized Approach Objective**|requirement.|||
|Scans by the malware solution are performed at a<br>frequency that addresses the entity’s risk.||||
|**Applicability Notes**||||
|This requirement applies to entities conducting<br>periodic malware scans to meet Requirement 5.3.2.<br>_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._||||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 128_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**5.3.3**For removable electronic media, the anti-<br>malware solution(s):<br>•<br>Performs automatic scans of when the media is<br>inserted, connected, or logically mounted,<br>**OR**|**5.3.3.a**Examine anti-malware solution(**s)**<br>configurations to verify that, for removable<br>electronic media, the solution is configured to<br>perform at least one of the elements specified in<br>this requirement.|Portable media devices are often overlooked as an<br>entry method for malware. Attackers will often pre-<br>load malware onto portable devices such as USB<br>and flash drives; connecting an infected device to a<br>computer then triggers the malware, introducing<br>new threats within the environment.|
|•<br>Performs continuous behavioral analysis of<br>systems or processes when the media is<br>inserted, connected, or logically mounted.|**5.3.3.b**Examine system components with<br>removable electronic media connected to verify<br>that the solution(s) is enabled in accordance with<br>at least one of the elements as specified in this<br>requirement.||
|**Customized Approach Objective**|**5.3.3.c**Examine logs and scan results to verify that<br>the solution(s) is enabled in accordance with at<br>least one of the elements specified in this<br>requirement.||
|Malware cannot be introduced to system<br>components via external removable media.|||
|**Applicability Notes**|||
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 129_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**5.3.4**Audit logs for the anti-malware solution(s) are<br>enabled and retained in accordance with<br>Requirement 10.5.1.<br>**Customized Approach Objective**<br>Historical records of anti-malware actions are<br>immediately available and retained for at least 12<br>months.|**5.3.4**Examine anti-malware solution(s)<br>configurations to verify logs are enabled and<br>retained in accordance with Requirement 10.5.1.|It is important to track the effectiveness of the anti-<br>malware mechanisms—for example, by confirming<br>that updates and scans are being performed as<br>expected, and that malware is identified and<br>addressed. Audit logs also allow an entity to<br>determine how malware entered the environment<br>and track its activity when inside the entity’s<br>network.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 130_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**5.3.5**Anti-malware mechanisms cannot be disabled<br>or altered by users, unless specifically documented,<br>and authorized by management on a case-by-case<br>basis for a limited time period.|**5.3.5.a**Examine anti-malware configurations, to<br>verify that the anti-malware mechanisms cannot be<br>disabled or altered by users.|It is important that defensive mechanisms are<br>always running so that malware is detected in real<br>time. Ad-hoc starting and stopping of anti-malware<br>solutions could allow malware to propagate<br>unchecked and undetected.|
|**Customized Approach Objective**<br>Anti-malware mechanisms cannot be modified by<br>unauthorized personnel.<br>**Applicability Notes**|**5.3.5.b**Interview responsible personnel and<br>observe processes to verify that any requests to<br>disable or alter anti-malware mechanisms are<br>specifically documented and authorized by<br>management on a case-by-case basis for a limited<br>time period.|**Good Practice**<br>Where there is a legitimate need to temporarily<br>disable a system’s anti-malware protection—for<br>example, to support a specific maintenance activity<br>or investigation of a technical problem—the reason<br>for taking such action should be understood and<br>approved by an appropriate management|
|Anti-malware solutions may be temporarily disabled<br>only if there is a legitimate technical need, as<br>authorized by management on a case-by-case<br>basis. If anti-malware protection needs to be<br>disabled for a specific purpose, it must be formally<br>authorized. Additional security measures may also<br>need to be implemented for the period during which<br>anti-malware protection is not active.||representative. Any disabling or altering of anti-<br>malware mechanisms, including on administrators’<br>own devices, should be performed by authorized<br>personnel. It is recognized that administrators have<br>privileges that may allow them to disable anti-<br>malware on their own computers, but there should<br>be alerting mechanisms in place when such<br>software is disabled and then follow up that occurs<br>to ensure correct processes were followed.<br>**Examples**<br>Additional security measures that may need to be<br>implemented for the period during which anti-<br>malware protection is not active include<br>disconnecting the unprotected system from the<br>Internet while the anti-malware protection is<br>disabled and running a full scan once it is re-<br>enabled.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 131_ 



###### **Requirements and Testing Procedures Guidance** 

###### **5.4 Anti-phishing mechanisms protect users against phishing attacks.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**5.4.1**Processes and automated mechanisms are in<br>place to detect and protect personnel against<br>phishing attacks.|**5.4.1**Observe implemented processes and<br>examine mechanisms to verify controls are in place<br>to detect and protect personnel against phishing<br>attacks.|Technical controls can limit the number of occasions<br>personnel have to evaluate the veracity of a<br>communication and can also limit the effects of<br>individual responses to phishing.|
|**Customized Approach Objective**||**Good Practice**<br>When developing anti-phishing controls, entities are|
|Mechanisms are in place to protect against and<br>mitigate risk posed by phishing attacks.||encouraged to consider a combination of<br>approaches. For example, using anti-spoofing<br>controls such as Domain-based Message|
|**Applicability Notes**||Authentication, Reporting & Conformance<br>(DMARC), Sender Policy Framework (SPF), and|
|The focus of this requirement is on protecting<br>personnel with access to system components in-<br>scope for PCI DSS.||Domain Keys Identified Mail (DKIM) will help stop<br>phishers from spoofing the entity’s domain and<br>impersonating personnel.|
|Meeting this requirement for technical and<br>automated controls to detect and protect personnel<br>against phishing is not the same as Requirement<br>12.6.3.1 for security awareness training. Meeting<br>this requirement does not also meet the requirement<br>for providing personnel with security awareness<br>training, and vice versa.<br>_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._||The deployment of technologies for blocking<br>phishing emails and malware before they reach<br>personnel, such as link scrubbers and server-side<br>anti-malware, can reduce incidents and decrease<br>the time required by personnel to check and report<br>phishing attacks. Additionally, training personnel to<br>recognize and report phishing emails can allow<br>similar emails to be identified and permit them to be<br>removed before being opened.<br>It is recommended (but not required) that anti-<br>phishing controls are applied across an entity’s<br>entire organization.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 132_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**5.4.1**_(continued)_||**Definitions**<br>Phishing is a form of social engineering and<br>describes the different methods used by attackers to<br>trick personnel into disclosing sensitive information,<br>such as user account names and passwords, and<br>account data. Attackers will typically disguise<br>themselves and attempt to appear as a genuine or<br>trusted source, directing personnel to send an email<br>response, click on a web link, or enter data into a<br>compromised website. Mechanisms that can detect<br>and prevent phishing attempts are often included in<br>anti-malware solutions.<br>**Further Information**<br>See the following for more information about<br>phishing:<br>_National Cyber Security Centre - Phishing Attacks:_<br>_Defending your Organization_.<br>_US Cybersecurity & Infrastructure Security Agency -_<br>_Report Phishing Sites._|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 133_ 



#### **_Requirement 6: Develop and Maintain Secure Systems and Software_** 

###### **Sections** 

- **6.1** Processes and mechanisms for developing and maintaining secure systems and software are defined and understood. 

- **6.2** Bespoke and custom software are developed securely. 

- **6.3** Security vulnerabilities are identified and addressed. 

- **6.4** Public-facing web applications are protected against attacks. 

- **6.5** Changes to all system components are managed securely. 

###### **Overview** 

Actors with bad intentions can use security vulnerabilities to gain privileged access to systems. Many of these vulnerabilities are fixed by vendor provided security patches, which must be installed by the entities that manage the systems. All system components must have all appropriate software patches to protect against the exploitation and compromise of account data by malicious individuals and malicious software. 

Appropriate software patches are those patches that have been evaluated and tested sufficiently to determine that the patches do not conflict with existing security configurations. For bespoke and custom software, numerous vulnerabilities can be avoided by applying software lifecycle (SLC) processes and secure coding techniques. 

Code repositories that store application code, system configurations, or other configuration data that can impact the security of cardholder data and/or sensitive authentication data are in scope for PCI DSS assessments. 

See _Relationship between PCI DSS and PCI SSC Software Standards_ on page 7 for information about the use of PCI SSC-validated software and software vendors, and how use of PCI SSC’s software standards may help with meeting controls in Requirement 6. Refer to _Appendix G_ for definitions of PCI DSS terms. 

**_<mark>Note</mark>_** _<mark>: Requirement 6 applies to all system components, except for section 6.2 for developing software securely, which applies only to bespoke and custom software used on any system component included in or connected to the CDE.</mark>_ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 134_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **6.1 Processes and mechanisms for developing and maintaining secure systems and software are defined and understood.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**6.1.1**All security policies and operational<br>procedures that are identified in Requirement 6 are:<br>•<br>Documented.<br>•<br>Kept up to date.<br>•<br>In use.<br>•<br>Known to all affected parties.|**6.1.1**Examine documentation and interview<br>personnel to verify that security policies and<br>operational procedures identified in Requirement 6<br>are managed in accordance with all elements<br>specified in this requirement.|Requirement 6.1.1 is about effectively managing and<br>maintaining the various policies and procedures<br>specified throughout Requirement 6. While it is<br>important to define the specific policies or procedures<br>called out in Requirement 6, it is equally important to<br>ensure they are properly documented, maintained,<br>and disseminated.<br>**Good Practice**<br>It is important to update policies and procedures as<br>needed to address changes in processes,|
|**Customized Approach Objective**||technologies, and business objectives. For this<br>reason, consider updating these documents as soon|
|Expectations, controls, and oversight for meeting<br>activities within Requirement 6 are defined and<br>adhered to by affected personnel. All supporting<br>activities are repeatable, consistently applied, and<br>conform to management’s intent.||as possible after a change occurs and not only on a<br>periodic cycle.<br>**Definitions**<br>Security policies define the entity’s security<br>objectives and principles. Operational procedures<br>describe how to perform activities, and define the<br>controls, methods, and processes that are followed to<br>achieve the desired result in a consistent manner and<br>in accordance with policy objectives.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 135_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**6.1.2**Roles and responsibilities for performing<br>activities in Requirement 6 are documented,<br>assigned, and understood.|**6.1.2.a**Examine documentation to verify that<br>descriptions of roles and responsibilities for<br>performing activities in Requirement 6 are<br>documented and assigned.<br>**6.1.2.b**Interview personnel responsible for<br>performing activities in Requirement 6 to verify that|If roles and responsibilities are not formally assigned,<br>systems will not be securely maintained, and their<br>security level will be reduced.<br>**Good Practice**<br>Roles and responsibilities may be documented within<br>policies and procedures or maintained within<br>separate documents.|
|**Customized Approach Objective**|roles and responsibilities are assigned as<br>documented and are understood.|As part of communicating roles and responsibilities,<br>entities can consider having personnel acknowledge|
|Day-to-day responsibilities for performing all the<br>activities in Requirement 6 are allocated. Personnel<br>are accountable for successful, continuous<br>operation of these requirements.||their acceptance and understanding of their assigned<br>roles and responsibilities.<br>**Examples**<br>A method to document roles and responsibilities is a<br>responsibility assignment matrix that includes who is<br>responsible, accountable, consulted, and informed<br>(also called a RACI matrix).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 136_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**6.2 Bespoke and custom software are develope**|**d securely.**||
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**6.2.1**Bespoke and custom software are developed<br>securely, as follows:<br>•<br>Based on industry standards and/or best<br>practices for secure development.<br>•<br>In accordance with PCI DSS (for example,<br>secure authentication and logging).<br>•<br>Incorporating consideration of information<br>security issues during each stage of the<br>software development lifecycle.|**6.2.1**Examine documented software development<br>procedures to verify that processes are defined<br>that include all elements specified in this<br>requirement.|Without the inclusion of security during the<br>requirements definition, design, analysis, and testing<br>phases of software development, security<br>vulnerabilities can be inadvertently or maliciously<br>introduced into the production environment.<br>**Good Practice**<br>Understanding how sensitive data is handled by the<br>application—including when stored, transmitted, and<br>in memory—can help identify where data needs to be<br>protected.|
|**Customized Approach Objective**<br>Bespoke and custom software is developed in<br>accordance with PCI DSS and secure development<br>processes throughout the software lifecycle.||PCI DSS requirements must be considered when<br>developing software to meet those requirements by<br>design, rather than trying to retrofit the software later.<br>**Examples**<br>Secure software lifecycle management<br>methodologies and frameworks include PCI Software|
|**Applicability Notes**||Security Framework, BSIMM, OPENSAMM, and<br>works from NIST, ISO, and SAFECode.|
|This applies to all software developed for or by the<br>entity for the entity’s own use. This includes both<br>bespoke and custom software. This does not apply<br>to third-party software.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 137_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**6.2.2**Software development personnel working on<br>bespoke and custom software are trained at least<br>once every 12 months as follows:<br>•<br>On software security relevant to their job<br>function and development languages.|**6.2.2.a**Examine software development procedures<br>to verify that processes are defined for training of<br>software development personnel developing<br>bespoke and custom software that includes all<br>elements specified in this requirement.|Having staff knowledgeable in secure coding<br>methods, including techniques defined in<br>Requirement 6.2.4, will help minimize the number of<br>security vulnerabilities introduced through poor<br>coding practices.<br>**Good Practice**|
|•<br>Including secure software design and secure<br>coding techniques.<br>|**6.2.2.b**Examine training records and interview<br>personnel to verify that software development|Training for developers may be provided in-house or<br>by third parties.|
|•<br>Including, if security testing tools are used, how<br>to use the tools for detecting vulnerabilities in<br>software.|<br>personnel working on bespoke and custom<br>software received software security training that is<br>relevant to their job function and development|Training should include, but is not limited to,<br>development languages in use, secure software<br>design, secure coding techniques, use of|
|**Customized Approach Objective**<br>Software development personnel remain<br>knowledgeable about secure development<br>practices; software security; and attacks against the<br>languages, frameworks, or applications they<br>develop. Personnel are able to access assistance<br>and guidance when required.|languages in accordance with all elements<br>specified in this requirement.|techniques/methods for finding vulnerabilities in<br>code, processes to prevent reintroducing previously<br>resolved vulnerabilities, and how to use any<br>automated security testing tools for detecting<br>vulnerabilities in software.<br>As industry-accepted secure coding practices<br>change, organizational coding practices and<br>developer training may need to be updated to<br>address new threats.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 138_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**6.2.3**Bespoke and custom software is reviewed<br>prior to being released into production or to<br>customers, to identify and correct potential coding<br>vulnerabilities, as follows:<br>•<br>Code reviews ensure code is developed<br>according to secure coding guidelines.|**6.2.3.a**Examine documented software<br>development procedures and interview responsible<br>personnel to verify that processes are defined that<br>require all bespoke and custom software to be<br>reviewed in accordance with all elements specified<br>in this requirement.|Security vulnerabilities in bespoke and custom<br>software are commonly exploited by malicious<br>individuals to gain access to a network and<br>compromise account data.<br>Vulnerable code is far more difficult and expensive to<br>address after it has been deployed or released into<br>production environments. Requiring a formal review|
|•<br>Code reviews look for both existing and<br>emerging software vulnerabilities.<br>•<br>Appropriate corrections are implemented prior to<br>release.|**6.2.3.b**Examine evidence of changes to bespoke<br>and custom software to verify that the code<br>changes were reviewed in accordance with all<br>elements specified in this requirement.|and signoff by management prior to release helps to<br>ensure that code is approved and has been<br>developed in accordance with policies and<br>procedures.<br>**Good Practice**|
|**Customized Approach Objective**||The following items should be considered for<br>inclusion in code reviews:|
|Bespoke and custom software cannot be exploited<br>via coding vulnerabilities.||•<br>Searching for undocumented features (implant<br>tools, backdoors).|
|**Applicability Notes**||•<br>Confirming that software securely uses external<br>components’ functions (libraries, frameworks,|
|This requirement for code reviews applies to all<br>bespoke and custom software (both internal and<br>public facing), as part of the system development<br>lifecycle.<br>Public-facing web applications are also subject to<br>additional controls, to address ongoing threats and<br>vulnerabilities after implementation, as defined at<br>PCI DSS Requirement 6.4.<br>Code reviews may be performed using either<br>manual or automated processes, or a combination<br>of both||APIs, etc.). For example, if a third-party library<br>providing cryptographic functions is used, verify<br>that it was integrated securely.<br>•<br>Checking for correct use of logging to prevent<br>sensitive data from getting into logs.<br>•<br>Analysis of insecure code structures that may<br>contain potential vulnerabilities related to<br>common software attacks identified in<br>Requirement 6.2.4.<br>•<br>Checking the application’s behavior to detect<br>logical vulnerabilities.|



Bespoke and custom software cannot be exploited via coding vulnerabilities. **Applicability Notes** This requirement for code reviews applies to all bespoke and custom software (both internal and public facing), as part of the system development lifecycle. Public-facing web applications are also subject to additional controls, to address ongoing threats and vulnerabilities after implementation, as defined at PCI DSS Requirement 6.4. Code reviews may be performed using either manual or automated processes, or a combination of both. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 139_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**6.2.3.1**If manual code reviews are performed for<br>bespoke and custom software prior to release to<br>production, code changes are:<br>•<br>Reviewed by individuals other than the<br>originating code author, and who are<br>knowledgeable about code-review techniques<br>and secure coding practices.<br>•<br>Reviewed and approved by management prior|**6.2.3.1.a**If manual code reviews are performed for<br>bespoke and custom software prior to release to<br>production, examine documented software<br>development procedures and interview responsible<br>personnel to verify that processes are defined for<br>manual code reviews to be conducted in<br>accordance with all elements specified in this<br>requirement.|Having code reviewed by someone other than the<br>original author, who is both experienced in code<br>reviews and knowledgeable about secure coding<br>practices, minimizes the possibility that code<br>containing security or logic errors that could affect the<br>security of cardholder data is released into a<br>production environment. Requiring management<br>approval that the code was reviewed limits the ability<br>for the process to be bypassed.|
|to release.<br>**Customized Approach Objective**|**6.2.3.1.b**Examine evidence of changes to<br>bespoke and custom software and interview<br>personnel to verify that manual code reviews were<br>conducted in accordance with all elements|**Good Practice**<br>Having a formal review methodology and review<br>checklists has been found to improve the quality of<br>the code review process.|
|The manual code review process cannot be<br>bypassed and is effective at discovering security<br>vulnerabilities.|specified in this requirement.|Code review is a tiring process, and for this reason, it<br>is most effective when reviewers only review small<br>amounts of code at a time.|
|**Applicability Notes**||To maintain the effectiveness of code reviews, it is<br>beneficial to monitor the general workload of|
|Manual code reviews can be conducted by<br>knowledgeable internal personnel or knowledgeable<br>third-party personnel.<br>An individual that has been formally granted<br>accountability for release control and who is neither<br>the original code author nor the code reviewer fulfills<br>the criteria of being management.||reviewers and to have them review applications they<br>are familiar with.<br>Code reviews may be performed using either manual<br>or automated processes, or a combination of both.<br>Entitles that rely solely on manual code review<br>should ensure that reviewers maintain their skills<br>through regular training as new vulnerabilities are<br>found, and new secure coding methods are<br>recommended.<br>**Further Information**<br>See the_OWASP Code Review Guide_.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 140_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**<br>**6.2.4**Software engineering techniques or other<br>methods are defined and in use by software<br>|**Defined Approach Testing Procedures**<br>**6.2.4**Examine documented procedures and<br>interview responsible software development|**Purpose**<br>Detecting or preventing common errors that result in<br>vulnerable code as early as possible in the software<br>development process lowers the probability that such|
|---|---|---|
|development personnel to prevent or mitigate<br>common software attacks and related vulnerabilities<br>in bespoke and custom software, including but not<br>limited to the following:|personnel to verify that software engineering<br>techniques or other methods are defined and in<br>use by developers of bespoke and custom<br>software to prevent or mitigate all common|errors make it through to production and lead to a<br>compromise. Having formal engineering techniques<br>and tools embedded in the development process will<br>catch these errors early. This philosophy is|
|•<br>Injection attacks, including SQL, LDAP, XPath,<br>or other command, parameter, object, fault, or<br>injection-type flaws.|software attacks as specified in this requirement.|sometimes called “shifting security left.”<br>**Good Practice**<br>For both bespoke and custom software, the entity|
|•<br>Attacks on data and data structures, including<br>attempts to manipulate buffers, pointers, input<br>data, or shared data.||must ensure that code is developed focusing on the<br>prevention or mitigation of common software attacks,<br>including:|
|•<br>Attacks on cryptography usage, including<br>attempts to exploit weak, insecure, or<br>inappropriate cryptographic implementations,<br>algorithms, cipher suites, or modes of operation.<br>•<br>Attacks on business logic, including attempts to||•<br>Attempts to exploit common coding vulnerabilities<br>(bugs).<br>•<br>Attempts to exploit software design flaws.<br>•<br>Attempts to exploit implementation/configuration<br>flaws.|



- Attacks on cryptography usage, including • Attempts to exploit common coding vulnerabilities attempts to exploit weak, insecure, or (bugs). inappropriate cryptographic implementations, • Attempts to exploit software design flaws. algorithms, cipher suites, or modes of operation. • Attempts to exploit implementation/configuration 

- • Attacks on business logic, including attempts to flaws. abuse or bypass application features and • Enumeration attacks – automated attacks that are 

- functionalities through the manipulation of APIs, actively exploited in payments and abuse 

- communication protocols and channels, clientidentification, authentication, or authorization 

- side functionality, or other system/application mechanisms. See the _PCI Perspectives blog_ 

- functions and resources. This includes cross-site _article “Beware of Account Testing Attacks_ .” 

- scripting (XSS) and cross-site request forgery _(continued on next page)_ 

- (CSRF). 

- • Attacks on access control mechanisms, including attempts to bypass or abuse identification, authentication, or authorization mechanisms, or attempts to exploit weaknesses in the implementation of such mechanisms. 

- • Attacks via any “high-risk” vulnerabilities identified in the vulnerability identification process, as defined in Requirement 6.3.1. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 141_ 



###### **Requirements and Testing Procedures Guidance** 

|**Customized Approach Objective**<br>Bespoke and custom software cannot be exploited<br>via common attacks and related vulnerabilities.|Researching and documenting software engineering<br>techniques or other methods helps to define how<br>software developers prevent or mitigate various<br>software attacks by features or countermeasures<br>they build into software. This might include|
|---|---|
|**Applicability Notes**|identification/authentication mechanisms, access<br>control, input validation routines, etc. Developers|
|This applies to all software developed for or by the|should be familiar with different types of|
|entity for the entity’s own use. This includes both<br>bespoke and custom software. This does not apply<br>to third-party software.|vulnerabilities and potential attacks and use<br>measures to avoid potential attack vectors when<br>developing code.|
||**Examples**|
||Techniques include automated processes and<br>practices that scan code early in the development<br>cycle when code is checked in to confirm the<br>vulnerabilities are not present.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 142_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**6.3 Security vulnerabilities are identified and ad**|**dressed.**||
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**6.3.1**Security vulnerabilities are identified and<br>managed as follows:<br>•<br>New security vulnerabilities are identified using<br>industry-recognized sources for security|**6.3.1.a**Examine policies and procedures for<br>identifying and managing security vulnerabilities to<br>verify that processes are defined in accordance<br>with all elements specified in this requirement.|Classifying the risks (for example, as critical, high,<br>medium, or low) allows organizations to identify,<br>prioritize, and address the highest risk items more<br>quickly and reduce the likelihood that vulnerabilities<br>posing the greatest risk will be exploited.|
|vulnerability information, including alerts from<br>international and national computer emergency<br>response teams (CERTs).<br>•<br>Vulnerabilities are assigned a risk ranking based<br>on industry best practices and consideration of<br>potential impact.<br>•<br>Risk rankings identify, at a minimum, all<br>vulnerabilities considered to be a high-risk or<br>critical to the environment.<br>•<br>Vulnerabilities for bespoke and custom, and<br>third-party software (for example operating<br>systems and databases) are covered.|**6.3.1.b**Interview responsible personnel, examine<br>documentation, and observe processes to verify<br>that security vulnerabilities are identified and<br>managed in accordance with all elements specified<br>in this requirement.|**Good Practice**<br>Methods for evaluating vulnerabilities and assigning<br>risk ratings will vary based on an organization’s<br>environment and risk-assessment strategy.<br>When an entity is assigning its risk rankings, it should<br>consider using a formal, objective, justifiable<br>methodology that accurately portrays the risks of the<br>vulnerabilities pertinent to the organization and<br>translates to an appropriate entity-assigned priority<br>for resolution.<br>Risk rankings should, at a minimum, identify all<br>vulnerabilities considered to be a “high risk” to the|
|**Customized Approach Objective**||environment. In addition to the risk ranking,<br>vulnerabilities may be considered “critical” if they|
|New system and software vulnerabilities that may<br>impact the security of cardholder data and/or<br>sensitive authentication data are monitored,<br>cataloged, and risk assessed.||pose an imminent threat to the environment, impact<br>critical systems, and/or would result in a potential<br>compromise if not addressed. Examples of critical<br>systems may include security systems, public-facing<br>devices and systems, databases, and other systems<br>that store, process, or transmit cardholder data.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 143_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Applicability Notes**|An organization’s processes for managing<br>vulnerabilities should be integrated with other|
|This requirement is not achieved by, and is in<br>addition to, performing vulnerability scans according<br>to Requirements 11.3.1 and 11.3.2. This<br>requirement is for a process to actively monitor<br>industry sources for vulnerability information and for<br>the entity to determine the risk ranking to be<br>associated with each vulnerability.|management processes—for example, risk<br>management, change management, patch<br>management, incident response, application security,<br>as well as proper monitoring and logging of these<br>processes. This process should include multiple<br>sources of vulnerability information, including<br>industry-recognized vulnerability databases (for<br>example, the US National Vulnerability Database),<br>CERTs, RSS feeds, information received from<br>vendors and third parties, and vulnerabilities<br>identified via internal and external vulnerability scans<br>(Requirements 11.3.1 and 11.3.2). This will help to<br>ensure all vulnerabilities are properly identified and<br>addressed. Processes should support ongoing<br>evaluation of vulnerabilities. For example, a<br>vulnerability initially identified as low risk could<br>become a higher risk later. Additionally,<br>vulnerabilities individually considered to be low or<br>medium risk, could collectively pose a high or critical<br>risk if present on the same system, or if exploited on<br>a low-risk system that could result in access to the<br>CDE.|
||_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 144_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**6.3.1**_(continued)_|**Examples**<br>Some organizations that issue alerts to advise<br>entities about urgent vulnerabilities requiring<br>immediate patches/updates are national Computer<br>Emergency Readiness/Response Teams (CERTs)<br>and vendors.<br>Criteria for ranking vulnerabilities may include<br>criticality of a vulnerability identified in an alert from<br>Forum of Incident Response and Security Teams<br>(FIRST) or a CERT, consideration of the CVSS<br>score, the classification by the vendor, and/or type of<br>systems affected.<br>**Further Information**<br>Trustworthy sources for vulnerability information<br>include vendor websites, industry newsgroups,<br>mailing lists, etc. If software is developed in-house,<br>the internal development team should also consider<br>sources of information about new vulnerabilities that<br>may affect internally developed applications. Other<br>methods to ensure new vulnerabilities are identified<br>include solutions that automatically recognize and<br>alert upon detection of unusual behavior. Processes<br>should account for widely published exploits as well<br>as “zero-day” attacks, which target previously<br>unknown vulnerabilities.<br>For bespoke and custom software, the organization<br>may obtain information about libraries, frameworks,<br>compilers, programming languages, etc. from public<br>trusted sources (for example, special resources and<br>resources from component developers). The<br>organization may also independently analyze third-<br>party components and identify vulnerabilities.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 145_ 



||**Requirements and Testing Procedures**|**Guidance**|
|---|---|---|
|**6.3.1**_(continued)_||For control over in-house developed software, the<br>organization may receive such information from<br>external sources. The organization can consider<br>using a “bug bounty” program where it posts<br>information (for example, on its website) so third<br>parties can contact the organization with vulnerability<br>information. External sources may include<br>independent investigators or companies that report to<br>the organization about identified vulnerabilities and<br>may include sources such as the Common<br>Vulnerability Scoring System (CVSS) or the OWASP<br>Risk Rating Methodology.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 146_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**6.3.2**An inventory of bespoke and custom software,<br>and third-party software components incorporated<br>into bespoke and custom software is maintained to<br>facilitate vulnerability and patch management.|**6.3.2.a**Examine documentation and interview<br>personnel to verify that an inventory of bespoke<br>and custom software and third-party software<br>components incorporated into bespoke and custom<br>software is maintained, and that the inventory is<br>used to identify and address vulnerabilities.|Identifying and listing all the entity’s bespoke and<br>custom software, and any third-party software that is<br>incorporated into the entity’s bespoke and custom<br>software enables the entity to manage vulnerabilities<br>and patches.<br>Vulnerabilities in third-party components (including<br>libraries, APIs, etc.) embedded in an entity’s software|
|**Customized Approach Objective**||also renders those applications vulnerable to attacks.<br>Knowing which third-party components are used in|
|Known vulnerabilities in third-party software<br>components cannot be exploited in bespoke and<br>custom software.|**6.3.2.b**Examine software documentation, including<br>for bespoke and custom software that integrates<br>third-party software components, and compare it to<br>the inventory to verify that the inventory includes<br>the bespoke and custom software and third-party<br>software components.|the entity’s software and monitoring the availability of<br>security patches to address known vulnerabilities is<br>critical to ensuring the security of the software.<br>**Good Practice**<br>An entity’s inventory should cover all payment<br>software components and dependencies, including|
|**Applicability Notes**||supported execution platforms or environments, third-<br>party libraries, services, and other required|
|_This requirement is a best practice until 31 March_||functionalities.|
|_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._||There are many different types of solutions that can<br>help with managing software inventories, such as<br>software composition analysis tools, application<br>discovery tools, and mobile device management.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 147_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**6.3.3**All system components are protected from<br>known vulnerabilities by installing applicable<br>security patches/updates as follows:<br>•<br>Patches/updates for critical vulnerabilities<br>(identified according to the risk ranking process|**6.3.3.a**Examine policies and procedures to verify<br>processes are defined for addressing<br>vulnerabilities by installing applicable security<br>patches/updates in accordance with all elements<br>specified in this requirement.|New exploits are constantly being discovered, and<br>these can permit attacks against systems that have<br>previously been considered secure. If the most<br>recent security patches/updates are not implemented<br>on critical systems as soon as possible, a malicious<br>actor can use these exploits to attack or disable a|
|at Requirement 6.3.1) are installed within one<br>month of release.<br>•<br>All other applicable security patches/updates are<br>installed within an appropriate time frame as<br>determined by the entity’s assessment of the<br>criticality of the risk to the environment as<br>identified according to the risk ranking process<br>at Requirement 6.3.1.|**6.3.3.b**Examine system components and related<br>software and compare the list of installed security<br>patches/updates to the most recent security<br>patch/update information to verify vulnerabilities<br>are addressed in accordance with all elements<br>specified in this requirement.|system or gain access to sensitive data.<br>**Good Practice**<br>Prioritizing security patches/updates for critical<br>infrastructure ensures that high-priority systems and<br>devices are protected from vulnerabilities as soon as<br>possible after a patch is released.<br>An entity’s patching cadence should factor in any re-<br>evaluation of vulnerabilities and subsequent changes|
|**Customized Approach Objective**||in the criticality of a vulnerability per Requirement<br>6.3.1. For example, a vulnerability initially identified|
|System components cannot be compromised via<br>the exploitation of a known vulnerability.||as low risk could become a higher risk later.<br>Additionally, vulnerabilities individually considered to<br>be low or medium risk could collectively pose a high<br>or critical risk if present on the same system, or if<br>exploited on a low-risk system that could result in<br>access to the CDE.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 148_ 



||**Requirements and Testing Procedures**|**Guidance**|
|---|---|---|
|**6.3.3**_(continued)_||It is recommended that the entity complete a targeted<br>risk analysis (TRA) according to PCI DSS<br>Requirement 12.3.1 to document the frequency of<br>installing all other applicable security<br>patches/updates. This TRA would include<br>consideration of the entity’s assessment of the<br>criticality of the risk to their environment as identified<br>in the risk ranking process at Requirement 6.3.1.<br>**Examples**<br>An example time frame for installation of<br>patches/updates could be 60 days for high-risk<br>vulnerabilities and 90 days for others, as determined<br>by the entity’s assessment of risk.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 149_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **6.4 Public-facing web applications are protected against attacks.** 

- **Defined Approach Requirements Defined Approach Testing Procedures Purpose** Public-facing web applications are those that are 

- **6.4.1** For public-facing web applications, new threats **6.4.1** For public-facing web applications, ensure available to the public (not only for internal use). and vulnerabilities are addressed on an ongoing that either one of the required methods is in place These applications are primary targets for attackers, basis and these applications are protected against as follows: and poorly coded web applications provide an easy known attacks as follows: • If manual or automated vulnerability security path for attackers to gain access to sensitive data • Reviewing public-facing web applications via assessment tools or methods are in use, and systems. manual or automated application vulnerability examine documented processes, interview **Good Practice** security assessment tools or methods as personnel, and examine records of application Manual or automated vulnerability security 

- follows: security assessments to verify that publicassessment tools or methods review and/or test the – At least once every 12 months and after facing web applications are reviewed in application for vulnerabilities. 

- significant changes. accordance with all elements of this Common assessment tools include specialized web 

- – By an entity that specializes in application requirement specific to the tool/method. scanners that perform automatic analysis of web 

- security. **OR** application protection. 

- – Including, at a minimum, all common • If an automated technical solution(s) is installed When using automated technical solutions, it is 

- software attacks in Requirement 6.2.4. that continually detects and prevents webimportant to include processes that facilitate timely 

- – All vulnerabilities are ranked in based attacks, examine the system responses to alerts generated by the solutions so 

- accordance with requirement 6.3.1. configuration settings and audit logs, and that any detected attacks can be mitigated. 

- – All vulnerabilities are corrected. interview responsible personnel to verify that **Examples** 

- – The application is re-evaluated after the the automated technical solution(s) is installed corrections. in accordance with all elements of this A web application firewall (WAF) installed in front of 

- **OR** requirement specific to the solution(s). public-facing web applications to check all traffic is an • Installing an automated technical solution(s) that example of an automated technical solution that detects and prevents web-based attacks (for 

- continually detects and prevents web-based attacks as follows: example, the attacks included in Requirement 6.2.4). WAFs filter and block non-essential traffic at the 

- – Installed in front of public-facing web application layer. A properly configured WAF helps to 

- applications to detect and prevent webprevent application-layer attacks on applications that 

- based attacks. are improperly coded or configured. 

- – Actively running and up to date as _(continued on next page)_ 

   - Actively running and up to date as applicable. 

   - – Generating audit logs. – Configured to either block web-based attacks or generate an alert that is immediately investigated. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 150_ 



###### **Requirements and Testing Procedures** 

**Customized Approach Objective** Public-facing web applications are protected against malicious attacks. **Applicability Notes** This assessment is not the same as the vulnerability scans performed for Requirement 11.3.1 and 11.3.2. _This requirement will be superseded by Requirement 6.4.2 after 31 March 2025 when Requirement 6.4.2 becomes effective._ 

###### **Guidance** 

|Another example of an automated technical solution|
|---|
|is Runtime Application Self-Protection (RASP)|
|technologies. When implemented correctly, RASP|
|solutions can detect and block anomalous behavior|
|by the software during execution. While WAFs|
|typically monitor the application perimeter, RASP<br>solutions monitor and block behavior within the<br>application.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 151_ 



###### **Requirements and Testing Procedures** 

**Defined Approach Requirements Defined Approach Testing Procedures 6.4.2** For public-facing web applications, an **6.4.2** For public-facing web applications, examine automated technical solution is deployed that the system configuration settings and audit logs, continually detects and prevents web-based attacks, and interview responsible personnel to verify that with at least the following: an automated technical solution that detects and • Is installed in front of public-facing web prevents web-based attacks is in place in applications and is configured to detect and accordance with all elements specified in this prevent web-based attacks. requirement. 

- Is installed in front of public-facing web applications and is configured to detect and prevent web-based attacks. 

- Actively running and up to date as applicable. 

- Generating audit logs. 

- • Configured to either block web-based attacks or generate an alert that is immediately investigated. 

###### **Guidance** 

###### **Purpose** 

Public-facing web applications are primary targets for attackers, and poorly coded web applications provide an easy path for attackers to gain access to sensitive data and systems. 

###### **Good Practice** 

When using automated technical solutions, it is important to include processes that facilitate timely responses to alerts generated by the solutions so that any detected attacks can be mitigated. Such solutions may also be used to automate mitigation, for example rate-limiting controls, which can be implemented to mitigate against brute-force attacks and enumeration attacks. 

###### **Examples** 

###### **Customized Approach Objective** 

Public-facing web applications are protected in real time against malicious attacks. **Applicability Notes** 

This new requirement will replace Requirement 6.4.1 once its effective date is reached. _This requirement is a best practice until 31 March 2025, after which it will be required and must be fully considered during a PCI DSS assessment._ 

A web application firewall (WAF), which can be either on-premise or cloud-based, installed in front of public-facing web applications to check all traffic, is an example of an automated technical solution that detects and prevents web-based attacks (for example, the attacks included in Requirement 6.2.4). WAFs filter and block non-essential traffic at the application layer. A properly configured WAF helps to prevent application-layer attacks on applications that are improperly coded or configured. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 152_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**6.4.3**All payment page scripts that are loaded and<br>executed in the consumer’s browser are managed<br>as follows:<br>•<br>A method is implemented to confirm that each<br>script is authorized.<br>•<br>A method is implemented to assure the integrity|**6.4.3.a**Examine policies and procedures to verify<br>that processes are defined for managing all<br>payment page scripts that are loaded and<br>executed in the consumer’s browser, in<br>accordance with all elements specified in this<br>requirement.|Scripts loaded and executed in the payment page<br>can have their functionality altered without the entity’s<br>knowledge and can also have the functionality to load<br>additional external scripts (for example, advertising<br>and tracking, tag management systems).<br>Such seemingly harmless scripts can be used by<br>potential attackers to upload malicious scripts that|
|of each script.<br>•<br>An inventory of all scripts is maintained with<br>written business or technical justification as to<br>why each is necessary.<br>**Customized Approach Objective**<br>Unauthorized code cannot be executed in the<br>payment page as it is rendered in the consumer’s<br>browser.|**6.4.3.b**Interview responsible personnel and<br>examine inventory records and system<br>configurations to verify that all payment page<br>scripts that are loaded and executed in the<br>consumer’s browser are managed in accordance<br>with all elements specified in this requirement.|can read and exfiltrate cardholder data from the<br>consumer browser.<br>Ensuring that the functionality of all such scripts is<br>understood to be necessary for the operation of the<br>payment page minimizes the number of scripts that<br>could be tampered with.<br>Ensuring that scripts have been explicitly authorized<br>reduces the probability of unnecessary scripts being<br>added to the payment page without appropriate<br>management approval. Where it is impractical for<br>such authorization to occur before a script is changed<br>or a new script is added to the page, the<br>authorization should be confirmed as soon as<br>possible after a change is made.<br>Using techniques to prevent tampering with the script<br>will minimize the probability of the script being<br>modified to carry out unauthorized behavior, such as<br>skimming the cardholder data from the payment<br>page.|
|||_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 153_ 



###### **Requirements and Testing Procedures** 

###### **Applicability Notes** 

This requirement applies to all scripts loaded from the entity’s environment and scripts loaded from third and fourth parties. 

This requirement also applies to scripts in the entity’s webpage(s) that includes a TPSP’s/ payment processor’s embedded payment page/form (for example, one or more inline frames or iframes). This requirement does not apply to an entity for scripts in a TPSP’s/payment processor’s embedded payment page/form (for example, one or more iframes), where the entity includes a TPSP’s/payment processor’s payment page/form on its webpage. Scripts in the TPSP’s/payment processor’s embedded payment page/form are the responsibility of the TPSP/payment processor to manage in accordance with this requirement. _This requirement is a best practice until 31 March 2025, after which it will be required and must be fully considered during a PCI DSS assessment._ 

###### **Guidance** 

###### **Good Practice** 

Scripts may be authorized by manual or automated (e.g., workflow) processes. Where the payment page will be loaded into an inline frame (iframe), restricting the location that the payment page can be loaded from, using the parent page’s Content Security Policy (CSP) can help prevent unauthorized content being substituted for the payment page. Where an entity includes a TPSP’s/payment processor’s embedded payment page/form on its webpage, the entity should expect the TPSP/payment processor to provide evidence that the TPSP/payment processor is meeting this requirement, in accordance with the TPSP’s/payment processor’s PCI DSS assessment and Requirement 12.9. **Examples** The integrity of scripts can be enforced by several different mechanisms including, but not limited to: • Sub-resource integrity (SRI), which allows the consumer browser to validate that a script has not been tampered with. • A CSP, which limits the locations the consumer browser can load a script from and transmit account data to. • Proprietary script or tag-management systems, which can prevent malicious script execution. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 154_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**6.5 Changes to all system components are managed securely.**|
|---|



|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**6.5.1**Changes to all system components in the<br>production environment are made according to<br>established procedures that include:<br>•<br>Reason for, and description of, the change.<br>•<br>Documentation of security impact.|**6.5.1.a**Examine documented change control<br>procedures to verify procedures are defined for<br>changes to all system components in the<br>production environment to include all elements<br>specified in this requirement.|Change management procedures must be applied to<br>all changes—including the addition, removal, or<br>modification of any system component—in the<br>production environment. It is important to document<br>the reason for a change and the change description<br>so that relevant parties understand and agree the<br>|
|•<br>Documented change approval by authorized<br>parties.|**6.5.1.b**Examine recent changes to system<br>components and trace those changes back to|change is needed. Likewise, documenting the<br>impacts of the change allows all affected parties to<br>plan appropriately for any processing changes.|
|•<br>Testing to verify that the change does not<br>adversely impact system security.<br>•<br>For bespoke and custom software changes, all<br>updates are tested for compliance with<br>Requirement 6.2.4 before being deployed into<br>production.<br>•<br>Procedures to address failures and return to a<br>secure state.|related change control documentation. For each<br>change examined, verify the change is<br>implemented in accordance with all elements<br>specified in this requirement.|<br>**Good Practice**<br>Approval by authorized parties confirms that the<br>change is legitimate and that the change is<br>sanctioned by the organization. Changes should be<br>approved by individuals with the appropriate authority<br>and knowledge to understand the impact of the<br>change.<br>Thorough testing by the entity confirms that the|
|**Customized Approach Objective**||security of the environment is not reduced by<br>implementing a change and that all existing security|
|All changes are tracked, authorized, and evaluated<br>for impact and security, and changes are managed<br>to avoid unintended effects to the security of system<br>components.||controls either remain in place or are replaced with<br>equal or stronger security controls after the change.<br>The specific testing to be performed will vary<br>according to the type of change and system<br>component(s) affected.<br>For each change, it is important to have documented<br>procedures that address any failures and provide<br>instructions on how to return to a secure state in case<br>the change fails or adversely affects the security of<br>an application or system. These procedures will allow<br>the application or system to be restored to its<br>previous secure state.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 155_ 



###### **Requirements and Testing Procedures** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|
|---|---|
|**6.5.2**Upon completion of a significant change, all<br>applicable PCI DSS requirements are confirmed to|**6.5.2**Examine documentation for significant<br>changes, interview personnel, and observe the|
|be in place on all new or changed systems and<br>networks, and documentation is updated as<br>applicable.|affected systems/networks to verify that the entity<br>confirmed applicable PCI DSS requirements were<br>in place on all new or changed systems and<br>networks and that documentation was updated as|
|**Customized Approach Objective**|applicable.|



All system components are verified after a significant change to be compliant with the applicable PCI DSS requirements. 

###### **Guidance** 

###### **Purpose** 

Having processes to analyze significant changes helps ensure that all appropriate PCI DSS controls are applied to any systems or networks added or changed within the in-scope environment, and that PCI DSS requirements continue to be met to secure the environment. 

###### **Good Practice** 

Building this validation into change management processes helps ensure that device inventories and configuration standards are kept up to date and security controls are applied where needed. 

###### **Examples** 

###### **Applicability Notes** 

These significant changes should also be captured and reflected in the entity’s annual PCI DSS scope confirmation activity per Requirement 12.5.2. 

Applicable PCI DSS requirements that could be impacted include, but are not limited to: 

- Network and data-flow diagrams are updated to reflect changes. 

- Systems are configured per configuration standards, with all default passwords changed and unnecessary services disabled. 

- Systems are protected with required controls—for example, file integrity monitoring (FIM), antimalware, patches, and audit logging. 

- Sensitive authentication data is not stored, and all account data storage is documented and incorporated into data retention policy and procedures. 

- New systems are included in the quarterly vulnerability scanning process. 

- Systems are scanned for internal and external vulnerabilities after significant changes per Requirements 11.3.1.3 and 11.3.2.1. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 156_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**6.5.3**Pre-production environments are separated<br>from production environments and the separation is<br>enforced with access controls.|**6.5.3.a**Examine policies and procedures to verify<br>that processes are defined for separating the pre-<br>production environment from the production<br>environment via access controls that enforce the<br>separation.|Due to the constantly changing state of pre-<br>production environments, they are often less secure<br>than the production environment.<br>**Good Practice**<br>Organizations must clearly understand which<br>environments are test environments or development|
||**6.5.3.b**Examine network documentation and<br>configurations of network security controls to verify<br>that the pre-production environment is separate<br>from the production environment(s).|environments and how these environments interact<br>on the level of networks and applications.<br>**Definitions**<br>Pre-production environments include development,<br>|
|**Customized Approach Objective**<br>Pre-production environments cannot introduce risks<br>and vulnerabilities into production environments.|**6.5.3.c**Examine access control settings to verify<br>that access controls are in place to enforce<br>separation between the pre-production and<br>production environment(s).|testing, user acceptance testing (UAT), etc. Even<br>where production infrastructure is used to facilitate<br>testing or development, production environments still<br>need to be separated (logically or physically) from<br>pre-production functionality such that vulnerabilities<br>introduced as a result of pre-production activities do<br>not adversely affect production systems.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 157_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**6.5.4**Roles and functions are separated between<br>production and pre-production environments to<br>provide accountability such that only reviewed and<br>approved changes are deployed.<br>**Customized Approach Objective**<br>Job roles and accountability that differentiate<br>between pre-production and production activities<br>are defined and managed to minimize the risk of<br>unauthorized, unintentional, or inappropriate<br>actions.|**6.5.4.a**Examine policies and procedures to verify<br>that processes are defined for separating roles and<br>functions to provide accountability such that only<br>reviewed and approved changes are deployed.<br>**6.5.4.b**Observe processes and interview<br>personnel to verify implemented controls separate<br>roles and functions and provide accountability such<br>that only reviewed and approved changes are<br>deployed.|The goal of separating roles and functions between<br>production and pre-production environments is to<br>reduce the number of personnel with access to the<br>production environment and account data and<br>thereby minimize risk of unauthorized, unintentional,<br>or inappropriate access to data and system<br>components and help ensure that access is limited to<br>those individuals with a business need for such<br>access.<br>The intent of this control is to separate critical<br>activities to provide oversight and review to catch<br>errors and minimize the chances of fraud or theft<br>(since two people would need to collude in order to<br>hide an activity).<br>Separating roles and functions, also referred to as|
|**Applicability Notes**||separation or segregation of duties, is a key internal<br>control concept to protect an entity’s assets.|
|In environments with limited personnel where<br>individuals perform multiple roles or functions, this<br>same goal can be achieved with additional<br>procedural controls that provide accountability. For<br>example, a developer may also be an administrator<br>that uses an administrator-level account with<br>elevated privileges in the development environment<br>and, for their developer role, they use a separate<br>account with user-level access to the production<br>environment.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 158_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**6.5.5**Live PANs are not used in pre-production<br>environments, except where those environments<br>are included in the CDE and protected in<br>accordance with all applicable PCI DSS<br>requirements.|**6.5.5.a**Examine policies and procedures to verify<br>that processes are defined for not using live PANs<br>in pre-production environments, except where<br>those environments are in a CDE and protected in<br>accordance with all applicable PCI DSS<br>requirements.|Use of live PANs outside of protected CDEs provides<br>malicious individuals with the opportunity to gain<br>unauthorized access to cardholder data.<br>**Definitions**<br>Live PANs refer to valid PANs (not test PANs) issued<br>by, or on behalf of, a payment brand.  Additionally,<br>when payment cards expire, the same PAN is often|
||**6.5.5.b**Observe testing processes and interview<br>personnel to verify procedures are in place to<br>ensure live PANs are not used in pre-production<br>environments, except where those environments<br>are in a CDE and protected in accordance with all<br>applicable PCI DSS requirements.|reused with a different expiry date. All PANs must be<br>verified as being unable to conduct payment<br>transactions or pose fraud risk to the payment<br>system before they are excluded from PCI DSS<br>scope. It is the responsibility of the entity to confirm<br>that PANs are not live.|
||**6.5.5.c**Examine pre-production test data to verify<br>live PANs are not used in pre-production||
|**Customized Approach Objective**|environments, except where those environments<br>are in a CDE and protected in accordance with all||
|Live PANs cannot be present in pre-production<br>environments outside the CDE.|applicable PCI DSS requirements.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 159_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**6.5.6**Test data and test accounts are removed from<br>system components before the system goes into<br>production.|**6.5.6.a**Examine policies and procedures to verify<br>that processes are defined for removal of test data<br>and test accounts from system components before<br>the system goes into production.<br>**6.5.6.b**Observe testing processes for both off-the-<br>shelf software and in-house applications, and<br>interview personnel to verify test data and test<br>accounts are removed before a system goes into<br>production.|This data may give away information about the<br>functioning of an application or system and is an<br>easy target for unauthorized individuals to exploit to<br>gain access to systems. Possession of such<br>information could facilitate compromise of the system<br>and related account data.|
|**Customized Approach Objective**<br>Test data and test accounts cannot exist in<br>production environments.|**6.5.6.c**Examine data and accounts for recently<br>installed or updated off-the-shelf software and in-<br>house applications to verify there is no test data or<br>test accounts on systems in production.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 160_ 



### **Implement Strong Access Control Measures** 

#### **_Requirement 7: Restrict Access to System Components and Cardholder Data by Business Need to Know_** 

**Sections** 

- **7.1** Processes and mechanisms for restricting access to system components and cardholder data by business need to know are defined and understood. 

- **7.2** Access to system components and data is appropriately defined and assigned. 

- **7.3** Access to system components and data is managed via an access control system(s). 

###### **Overview** 

Unauthorized individuals may gain access to critical data or systems due to ineffective access control rules and definitions. To ensure critical data can only be accessed by authorized personnel, systems and processes must be in place to limit access based on need to know and according to job responsibilities. 

“Access” or “access rights” are created by rules that provide users access to systems, applications, and data, while “privileges” allow a user to perform a specific action or function in relation to that system, application, or data. For example, a user may have access rights to specific data, but whether they can only read that data, or can also change or delete the data is determined by the user’s assigned privileges. 

“Need to know” refers to providing access to only the least amount of data needed to perform a job. 

“Least privileges” refers to providing only the minimum level of privileges needed to perform a job. 

These requirements apply to user accounts and access for employees, contractors, consultants, and internal and external vendors and other third parties (for example, for providing support or maintenance services). Certain requirements also apply to application and system accounts used by the entity (also called “service accounts”). 

**These requirements do not apply to consumers (cardholders)** . 

Refer to _Appendix G_ for definitions of PCI DSS terms. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 161_ 



###### **Requirements and Testing Procedures Guidance** 

**7.1 Processes and mechanisms for restricting access to system components and cardholder data by business need to know are defined and understood.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**7.1.1**All security policies and operational<br>procedures that are identified in Requirement 7 are:<br>•<br>Documented.<br>•<br>Kept up to date.<br>•<br>In use.<br>•<br>Known to all affected parties.|**7.1.1**Examine documentation and interview<br>personnel to verify that security policies and<br>operational procedures identified in Requirement 7<br>are managed in accordance with all elements<br>specified in this requirement.|Requirement 7.1.1 is about effectively managing<br>and maintaining the various policies and<br>procedures specified throughout Requirement 7.<br>While it is important to define the specific policies<br>or procedures called out in Requirement 7, it is<br>equally important to ensure they are properly<br>documented, maintained, and disseminated.<br>**Good Practice**|
|**Customized Approach Objective**||It is important to update policies and procedures<br>as needed to address changes in processes,|
|Expectations, controls, and oversight for meeting<br>activities within Requirement 7 are defined and<br>adhered to by affected personnel. All supporting<br>activities are repeatable, consistently applied, and<br>conform to management’s intent.||technologies, and business objectives. For this<br>reason, consider updating these documents as<br>soon as possible after a change occurs and not<br>only on a periodic cycle.<br>**Definitions**<br>Security policies define the entity’s security<br>objectives and principles. Operational procedures<br>describe how to perform activities, and define the<br>controls, methods, and processes that are<br>followed to achieve the desired result in a<br>consistent manner and in accordance with policy<br>objectives.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 162_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**7.1.2**Roles and responsibilities for performing<br>activities in Requirement 7 are documented,<br>assigned, and understood.|**7.1.2.a**Examine documentation to verify that<br>descriptions of roles and responsibilities for<br>performing activities in Requirement 7 are<br>documented and assigned.|If roles and responsibilities are not formally<br>assigned, personnel may not be aware of their<br>day-to-day responsibilities, and critical activities<br>may not occur.<br>**Good Practice**|
|**Customized Approach Objective**<br>Day-to-day responsibilities for performing all the<br>activities in Requirement 7 are allocated. Personnel<br>are accountable for successful, continuous<br>operation of these requirements.|**7.1.2.b**Interview personnel with responsibility for<br>performing activities in Requirement 7 to verify that<br>roles and responsibilities are assigned as and are<br>understood.|Roles and responsibilities may be documented<br>within policies and procedures or maintained<br>within separate documents.<br>As part of communicating roles and<br>responsibilities, entities can consider having<br>personnel acknowledge their acceptance and<br>understanding of their assigned roles and<br>responsibilities.<br>**Examples**<br>A method to document roles and responsibilities<br>is a responsibility assignment matrix that includes<br>who is responsible, accountable, consulted, and<br>informed (also called a RACI matrix).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 163_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **7.2 Access to system components and data is appropriately defined and assigned.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|
|---|---|
|**7.2.1**An access control model is defined and<br>includes granting access as follows:<br>•<br>Appropriate access depending on the entity’s<br>business and access needs.|**7.2.1.a**Examine documented policies and<br>procedures and interview personnel to verify the<br>access control model is defined in accordance with<br>all elements specified in this requirement.|
|•<br>Access to system components and data<br>resources that is based on users’ job<br>classification and functions.<br>•<br>The least privileges required (for example, user,<br>|**7.2.1.b**Examine access control model settings and<br>verify that access needs are appropriately defined<br>in accordance with all elements specified in this<br>requirement.|



- The least privileges required (for example, user, administrator) to perform a job function. 

###### **Customized Approach Objective** 

Access requirements are established according to job functions following least-privilege and need-toknow principles. 

###### **Purpose** 

Defining an access control model that is appropriate for the entity’s technology and access control philosophy supports a consistent and uniform way of allocating access and reduces the possibility of errors such as the granting of excessive rights. 

###### **Good Practice** 

A factor to consider when defining access needs is the separation of duties principle. This principle is intended to prevent fraud and misuse or theft of resources. For example, 1) dividing missioncritical functions and information system support functions among different individuals and/or functions, 2) establishing roles such that information system support activities are performed by different functions/individuals (for example, system management, programming, configuration management, quality assurance and testing, and network security), and 3) ensuring security personnel administering access control functions do not also administer audit functions. In environments where one individual performs multiple functions, such as administration and security operations, duties may be assigned so that no single individual has end-to-end control of a process without an independent checkpoint. For example, responsibility for configuration and responsibility for approving changes could be assigned to separate individuals. _(continued on next page)_ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 164_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**7.1.2**_(continued)_|**Definitions**<br>Key elements of an access control model include:<br>•<br>Resources to be protected (the<br>systems/devices/data to which access is<br>needed),<br>•<br>Job functions that need access to the<br>resource (for example, system administrator,<br>call-center personnel, store clerk), and<br>•<br>Which activities each job function needs to<br>perform (for example, read/write or query).<br>Once job functions, resources, and activities per<br>job functions are defined, individuals can be<br>granted access accordingly.<br>**Examples**<br>Access control models that entities can consider<br>include role-based access control (RBAC) and<br>attribute-based access control (ABAC). The<br>access control model used by a given entity<br>depends on their business and access needs.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 165_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**7.2.2**Access is assigned to users, including<br>privileged users, based on:<br>•<br>Job classification and function.<br>•<br>Least privileges necessary to perform job|**7.2.2.a**Examine policies and procedures to verify<br>they cover assigning access to users in<br>accordance with all elements specified in this<br>requirement.|Assigning least privileges helps prevent users<br>without sufficient knowledge about the application<br>from incorrectly or accidentally changing<br>application configuration or altering its security<br>settings. Enforcing least privilege also helps to<br>|
|responsibilities.|**7.2.2.b**Examine user access settings, including for<br>privileged users, and interview responsible<br>management personnel to verify that privileges<br>assigned are in accordance with all elements<br>specified in this requirement.|minimize the scope of damage if an unauthorized<br>person gains access to a user ID.<br>**Good Practice**<br>Access rights are granted to a user by<br>assignment to one or several functions. Access is<br>assigned depending on the specific user functions|
||**7.2.2.c**Interview personnel responsible for<br>assigning access to verify that privileged user|and with the minimum scope required for the job.<br>When assigning privileged access, it is important|
|**Customized Approach Objective**|access is assigned in accordance with all elements<br>specified in this requirement.|to assign individuals only the privileges they need<br>to perform their job (the “least privileges”). For|
|Access to systems and data is limited to only the<br>access needed to perform job functions, as defined<br>in the related access roles.||example, the database administrator or backup<br>administrator should not be assigned the same<br>privileges as the overall systems administrator.<br>Once needs are defined for user functions (per<br>PCI DSS requirement 7.2.1), it is easy to grant<br>individuals access according to their job<br>classification and function by using the already-<br>created roles.<br>Entities may wish to consider use of Privileged<br>Access Management (PAM), which is a method to<br>grant access to privileged accounts only when<br>those privileges are required, immediately<br>revoking that access once they are no longer<br>needed.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 166_ 



|**Requirements an**|**d Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**7.2.3**Required privileges are approved by<br>authorized personnel.|**7.2.3.a**Examine policies and procedures to verify<br>they define processes for approval of all privileges<br>by authorized personnel.|Documented approval (for example, in writing or<br>electronically) assures that those with access and<br>privileges are known and authorized by<br>management, and that their access is necessary|
||**7.2.3.b**Examine user IDs and assigned privileges,<br>and compare with documented approvals to verify|for their job function.|
|**Customized Approach Objective**|that:||
|Access privileges cannot be granted to users<br>without appropriate, documented authorization.|•<br>Documented approval exists for the assigned<br>privileges.<br>•<br>The approval was by authorized personnel.<br>•<br>Specified privileges match the roles assigned<br>to the individual.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 167_ 



###### **Requirements and Testing Procedures** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|
|---|---|
|**7.2.4**All user accounts and related access<br>privileges, including third-party/vendor accounts, are<br>reviewed as follows:<br>•<br>At least once every six months.<br>•<br>To ensure user accounts and access remain|**7.2.4.a**Examine policies and procedures to verify<br>they define processes to review all user accounts<br>and related access privileges, including third-<br>party/vendor accounts, in accordance with all<br>elements specified in this requirement.|
|appropriate based on job function.<br>•<br>Any inappropriate access is addressed.|**7.2.4.b**Interview responsible personnel and<br>examine documented results of periodic reviews of|
|•<br>Management acknowledges that access<br>remains appropriate.|user accounts to verify that all the results are in<br>accordance with all elements specified in this<br>requirement.|



###### **Customized Approach Objective** 

Account privilege assignments are verified periodically by management as correct, and nonconformities are remediated. **Applicability Notes** 

This requirement applies to all user accounts and related access privileges, including those used by personnel and third parties/vendors, and accounts used to access third-party cloud services. See Requirements 7.2.5 and 7.2.5.1 and 8.6.1 through 8.6.3 for controls for application and system accounts. 

_This requirement is a best practice until 31 March 2025, after which it will be required and must be fully considered during a PCI DSS assessment._ 

###### **Guidance** 

###### **Purpose** 

Regular review of access rights helps to detect excessive access rights remaining after user job responsibilities change, system functions change, or other modifications. If excessive user rights are not revoked in due time, they may be used by malicious users for unauthorized access. 

This review provides another opportunity to ensure that accounts for all terminated users have been removed (if any were missed at the time of termination), as well as to ensure that any third parties that no longer need access have had their access terminated. 

###### **Good Practice** 

When a user transfers into a new role or a new department, typically the privileges and access associated with their former role are no longer required. Continued access to privileges or functions that are no longer required may introduce the risk of misuse or errors. Therefore, when responsibilities change, processes that revalidate access help to ensure user access is appropriate for the user’s new responsibilities. Entities can consider implementing a regular, repeatable process for conducting reviews of access rights, and assigning “data owners” that are responsible for managing and monitoring access to data related to their job function and that also ensure user access remains current and appropriate. As an example, a direct manager could review team access monthly, while the senior manager reviews their groups’ access quarterly, both making updates to access as needed. The intent of these best practices is to support and facilitate conducting the reviews at least once every 6 months. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 168_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**7.2.5**All application and system accounts and<br>related access privileges are assigned and<br>managed as follows:|**7.2.5.a**Examine policies and procedures to verify<br>they define processes to manage and assign<br>application and system accounts and related<br>|It is important to establish the appropriate access<br>level for application or system accounts. If such<br>accounts are compromised, malicious users will<br>receive the same access level as that granted to|
|•<br>Based on the least privileges necessary for the<br>operability of the system or application.|access privileges in accordance with all elements<br>specified in this requirement.|the application or system. Therefore, it is<br>important to ensure limited access is granted to|
|•<br>Access is limited to the systems, applications, or<br>processes that specifically require their use.|**7.2.5.b**Examine privileges associated with system<br>and application accounts and interview responsible<br>personnel to verify that application and system|system and application accounts on the same<br>basis as to user accounts.<br>**Good Practice**|
|**Customized Approach Objective**|<br>accounts and related access privileges are<br>assigned and managed in accordance with all|Entities may want to consider establishing a<br>baseline when setting up these application and|
|Access rights granted to application and system<br>accounts are limited to only the access needed for|<br>elements specified in this requirement.|system accounts including the following as<br>applicable to the organization:|
|the operability of that application or system.||•<br>Making sure that the account is not a member<br>of a privileged group such as domain|
|**Applicability Notes**||administrators, local administrators, or root.<br>•<br>Restricting which computers the account can|
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_||be used on.<br>•<br>Restricting hours of use.|
|_fully considered during a PCI DSS assessment._||•<br>Removing any additional settings like VPN<br>access and remote access.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 169_ 



###### **Requirements and Testing Procedures** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|
|---|---|
|**7.2.5.1**All access by application and system<br>accounts and related access privileges are reviewed<br>as follows:<br>•<br>Periodically (at the frequency defined in the<br>entity’s targeted risk analysis, which is|**7.2.5.1.a**Examine policies and procedures to verify<br>they define processes to review all application and<br>system accounts and related access privileges in<br>accordance with all elements specified in this<br>requirement.|
|performed according to all elements specified in<br>Requirement 12.3.1).<br>•<br>The application/system access remains<br>appropriate for the function being performed.<br>•<br>Any inappropriate access is addressed.<br>•<br>Management acknowledges that access<br>remains appropriate.|**7.2.5.1.b**Examine the entity’s targeted risk<br>analysis for the frequency of periodic reviews of<br>application and system accounts and related<br>access privileges to verify the risk analysis was<br>performed in accordance with all elements<br>specified in Requirement 12.3.1.|
||**7.2.5.1.c**Interview responsible personnel and<br>examine documented results of periodic reviews of|
|**Customized Approach Objective**|system and application accounts and related<br>privileges to verify that the reviews occur in|
|Application and system account privilege<br>assignments are verified periodically by<br>management as correct, and nonconformities are<br>remediated.|accordance with all elements specified in this<br>requirement.|
|**Applicability Notes**||
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_||
|_fully considered during a PCI DSS assessment._||



###### **Guidance** 

**Purpose** Regular review of access rights helps to detect excessive access rights remaining after system functions change, or other application or system modifications occur. If excessive rights are not removed when no longer needed, they may be used by malicious users for unauthorized access. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 170_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**7.2.6**All user access to query repositories of stored<br>cardholder data is restricted as follows:<br>•<br>Via applications or other programmatic methods,<br>with access and allowed actions based on user<br>roles and least privileges.|**7.2.6.a**Examine policies and procedures and<br>interview personnel to verify processes are defined<br>for granting user access to query repositories of<br>stored cardholder data, in accordance with all<br>elements specified in this requirement.|The misuse of query access to repositories of<br>cardholder data has been a regular cause of data<br>breaches. Limiting such access to administrators<br>reduces the risk of such access being abused by<br>unauthorized users.<br>**Definitions**|
|•<br>Only the responsible administrator(s) can<br>directly access or query repositories of stored<br>CHD.|**7.2.6.b**Examine configuration settings for querying<br>repositories of stored cardholder data to verify they<br>are in accordance with all elements specified in|“Programmatic methods” means granting access<br>through means such as database stored<br>procedures that allow users to perform controlled<br>|
|**Customized Approach Objective**|this requirement.|actions to data in a table, rather than via direct,<br>unfiltered access to the data repository by end|
|Direct unfiltered (ad hoc) query access to<br>cardholder data repositories is prohibited, unless<br>performed by an authorized administrator.||users (except for the responsible administrator(s),<br>who need direct access to the database for their<br>administrative duties).<br>**Good Practice**|
|**Applicability Notes**<br>This requirement applies to controls for user access<br>to query repositories of stored cardholder data.<br>See Requirements 7.2.5 and 7.2.5.1 and 8.6.1<br>through 8.6.3 for controls for application and system<br>accounts.||Typical user actions include moving, copying, and<br>deleting data. Also consider the scope of privilege<br>needed when granting access. For example,<br>access can be granted to specific objects such as<br>data elements, files, tables, indexes, views, and<br>stored routines. Granting access to repositories of<br>cardholder data should follow the same process<br>as all other granted access, meaning that it is<br>based on roles, with only the privileges assigned<br>to each user that are needed to perform their job<br>functions.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 171_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **7.3 Access to system components and data is managed via an access control system(s).** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**7.3.1**An access control system(s) is in place that<br>restricts access based on a user’s need to know<br>and covers all system components.<br>**Customized Approach Objective**|**7.3.1**Examine vendor documentation and system<br>settings to verify that access is managed for each<br>system component via an access control system(s)<br>that restricts access based on a user’s need to<br>know and covers all system components.|Without a mechanism to restrict access based on<br>user’s need to know, a user may unknowingly be<br>granted access to cardholder data. Access control<br>systems automate the process of restricting<br>access and assigning privileges.|
|Access rights and privileges are managed via<br>mechanisms intended for that purpose.|||
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**7.3.2**The access control system(s) is configured to<br>enforce permissions assigned to individuals,<br>applications, and systems based on job<br>classification and function.|**7.3.2**Examine vendor documentation and system<br>settings to verify that the access control system(s)<br>is configured to enforce permissions assigned to<br>individuals, applications, and systems based on job<br>classification and function.|Restricting privileged access with an access<br>control system reduces the opportunity for errors<br>in the assignment of permissions to individuals,<br>applications, and systems.|
|**Customized Approach Objective**|||
|Individual account access rights and privileges to<br>systems, applications, and data are only inherited<br>from group membership.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 172_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**7.3.3**The access control system(s) is set to “deny<br>all” by default.|**7.3.3**Examine vendor documentation and system<br>settings to verify that the access control system(s)<br>is set to “deny all” by default.|A default setting of “deny all” ensures no one is<br>granted access unless a rule is established<br>specifically granting such access.<br>**Good Practice**|
|**Customized Approach Objective**<br>Access rights and privileges are prohibited unless<br>expressly permitted.||It is important to check the default configuration of<br>access control systems because some are set by<br>default to “allow all,” thereby permitting access<br>unless/until a rule is written to specifically deny it.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 173_ 



#### **_Requirement 8: Identify Users and Authenticate Access to System Components_** 

###### **Sections** 

- **8.1** Processes and mechanisms for identifying users and authenticating access to system components are defined and understood. 

- **8.2** User identification and related accounts for users and administrators are strictly managed throughout an account’s lifecycle. 

- **8.3** Strong authentication for users and administrators is established and managed. 

- **8.4** Multi-factor authentication (MFA) is implemented to secure access into the CDE. 

- **8.5** Multi-factor authentication (MFA) systems are configured to prevent misuse. 

- **8.6** Use of application and system accounts and associated authentication factors is strictly managed. 

###### **Overview** 

Two fundamental principles of identifying and authenticating users are to 1) establish the identity of an individual or process on a computer system, and 2) prove or verify the user associated with the identity is who the user claims to be. 

Identification of an individual or process on a computer system is conducted by associating an identity with a person or process through an identifier, such as a user, system, or application ID. These IDs (also referred to as “accounts”) fundamentally establish the identity of an individual or process by assigning unique identification to each person or process to distinguish one user or process from another. When each user or process can be uniquely identified, it ensures there is accountability for actions performed by that identity. When such accountability is in place, actions taken can be traced to known and authorized users and processes. 

The element used to prove or verify the identity is known as the authentication factor. Authentication factors are 1) something you know, such as a password or passphrase, 2) something you have, such as a token device or smart card, or 3) something you are, such as a biometric element. 

The ID and the authentication factor together are considered authentication credentials and are used to gain access to the rights and privileges associated with a user, application, system, or service accounts. 

These requirements for identity and authentication are based on industry-accepted security principles and best practices to support the payment ecosystem. _NIST Special Publication 800-63, Digital Identity Guidelines_ provides additional information on acceptable frameworks for digital identity and authentication factors. It is important to note that the _NIST Digital Identity Guidelines_ is intended for US Federal Agencies and should be viewed in its entirety.  Many of the concepts and approaches defined in these guidelines are expected to work with each other and not as standalone parameters. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 174_ 



**_Note_** _: Unless otherwise stated in the requirement, these requirements apply to_ **_all accounts on all system components_** _, unless specifically called out in an individual requirement, including but not limited to:_ 

- _Point-of-sale accounts_ 

- _Accounts with administrative capabilities_ 

- _System and application accounts_ 

- _All accounts used to view or access cardholder data or to access systems with cardholder data._ 

_This includes accounts used by employees, contractors, consultants, internal and external vendors, and other third parties (for example, for providing support or maintenance services)._ 

_Certain requirements are not intended to apply to user accounts on point-of-sale terminals that have access to only one card number at a time to facilitate a single transaction. When items do not apply, they are noted directly within the specific requirement._ 

###### **These requirements do not apply to accounts used by consumers (cardholders).** 

_Refer to_ Appendix G _for definitions of PCI DSS terms._ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 175_ 



###### **Requirements and Testing Procedures Guidance** 

###### **8.1 Processes and mechanisms for identifying users and authenticating access to system components are defined and understood.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**8.1.1**All security policies and operational<br>procedures that are identified in Requirement 8 are:<br>•<br>Documented.<br>•<br>Kept up to date.<br>•<br>In use.<br>•<br>Known to all affected parties.|**8.1.1**Examine documentation and interview<br>personnel to verify that security policies and<br>operational procedures that are identified in<br>Requirement 8 are managed in accordance with all<br>elements specified in this requirement.|Requirement 8.1.1 is about effectively managing<br>and maintaining the various policies and<br>procedures specified throughout Requirement 8.<br>While it is important to define the specific policies<br>or procedures called out in Requirement 8, it is<br>equally important to ensure they are properly<br>documented, maintained, and disseminated.<br>**Good Practice**|
|**Customized Approach Objective**||It is important to update policies and procedures<br>as needed to address changes in processes,|
|Expectations, controls, and oversight for meeting<br>activities within Requirement 8 are defined and<br>adhered to by affected personnel. All supporting<br>activities are repeatable, consistently applied, and<br>conform to management’s intent.||technologies, and business objectives. For this<br>reason, consider updating these documents as<br>soon as possible after a change occurs and not<br>only on a periodic cycle.<br>**Definitions**<br>Security policies define the entity’s security<br>objectives and principles. Operational procedures<br>describe how to perform activities, and define the<br>controls, methods, and processes that are<br>followed to achieve the desired result in a<br>consistent manner and in accordance with policy<br>objectives.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 176_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**8.1.2**Roles and responsibilities for performing<br>activities in Requirement 8 are documented,<br>assigned, and understood.|**8.1.2.a**Examine documentation to verify that<br>descriptions of roles and responsibilities for<br>performing activities in Requirement 8 are<br>documented and assigned.|If roles and responsibilities are not formally<br>assigned, personnel may not be aware of their<br>day-to-day responsibilities and critical activities<br>may not occur.<br>**Good Practice**|
||**8.1.2.b**Interview personnel with responsibility for<br>performing activities in Requirement 8 to verify that|Roles and responsibilities may be documented<br>within policies and procedures or maintained<br>|
|**Customized Approach Objective**|roles and responsibilities are assigned as<br>documented and are understood.|within separate documents.<br>As part of communicating roles and|
|Day-to-day responsibilities for performing all the<br>activities in Requirement 8 are allocated. Personnel<br>are accountable for successful, continuous<br>operation of these requirements.||responsibilities, entities can consider having<br>personnel acknowledge their acceptance and<br>understanding of their assigned roles and<br>responsibilities.<br>**Examples**<br>A method to document roles and responsibilities<br>is a responsibility assignment matrix that includes<br>who is responsible, accountable, consulted, and<br>informed (also called a RACI matrix).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 177_ 



###### **Requirements and Testing Procedures Guidance** 

###### **8.2 User identification and related accounts for users and administrators are strictly managed throughout an account’s lifecycle.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**8.2.1**All users are assigned a unique ID before<br>access to system components or cardholder data is<br>allowed.|**8.2.1.a**Interview responsible personnel to verify<br>that all users are assigned a unique ID for access<br>to system components and cardholder data.|The ability to trace actions performed on a<br>computer system to an individual establishes<br>accountability and traceability and is fundamental<br>to establishing effective access controls.|
||**8.2.1.b**Examine audit logs and other evidence to<br>verify that access to system components and|By ensuring each user is uniquely identified,<br>instead of using one ID for several employees, an|
|**Customized Approach Objective**<br>All actions by all users are attributable to an<br>individual.|<br>cardholder data can be uniquely identified and<br>associated with individuals.|organization can maintain individual responsibility<br>for actions and an effective record in the audit log<br>per employee. In addition, this will assist with<br>issue resolution and containment when misuse or<br>malicious intent occurs.|
|**Applicability Notes**|||
|This requirement is not intended to apply to user<br>accounts within point-of-sale terminals that have<br>access to only one card number at a time to<br>facilitate a single transaction|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 178_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**8.2.2**Group, shared, or generic IDs, or other shared<br>authentication credentials are only used when<br>necessary on an exception basis, and are managed<br>as follows:|**8.2.2.a**Examine user account lists on system<br>components and applicable documentation to<br>verify that shared authentication credentials are<br>only used when necessary, on an exception basis,<br>|Group, shared, or generic (or default) IDs are<br>typically delivered with software or operating<br>systems—for example, root or with privileges<br>associated with a specific function, such as an<br>administrator.|
|•<br>ID use is prevented unless needed for an<br>exceptional circumstance.<br>|and are managed in accordance with all elements<br>specified in this requirement.|If multiple users share the same authentication<br>credentials (for example, user ID and password),|
|•<br>Use is limited to the time needed for the<br>exceptional circumstance.<br>•<br>Business justification for use is documented.<br>•<br>Use is explicitly approved by management.<br>•<br>Individual user identity is confirmed before<br>access to an account is granted.<br>|**8.2.2.b**Examine authentication policies and<br>procedures to verify processes are defined for<br>shared authentication credentials such that they<br>are only used when necessary, on an exception<br>basis, and are managed in accordance with all<br>elements specified in this requirement.|it becomes impossible to trace system access<br>and activities to an individual. In turn, this<br>prevents an entity from assigning accountability<br>for, or having effective logging of, an individual’s<br>actions since a given action could have been<br>performed by anyone in the group with knowledge<br>of the user ID and associated authentication|
|•<br>Every action taken is attributable to an individual<br>user.<br>**Customized Approach Objective**|**8.2.2.c**Interview system administrators to verify<br>that shared authentication credentials are only<br>used when necessary, on an exception basis, and<br>are managed in accordance with all elements<br>specified in this requirement.|factors.<br>The ability to associate individuals to the actions<br>performed with an ID is essential to provide<br>individual accountability and traceability regarding<br>who performed an action, what action was<br>performed, and when that action occurred.|
|All actions performed by users with group, shared,<br>or generic IDs are attributable to an individual<br>person.||**Good Practice**<br>If shared IDs are used for any reason, strong<br>management controls need to be established to|
|**Applicability Notes**||maintain individual accountability and traceability.<br>_(continued on next page)_|



|**Applicability Notes**|
|---|
|This requirement is not intended to apply to user<br>accounts within point-of-sale terminals that have<br>access to only one card number at a time to|
|facilitate a single transaction.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 179_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**8.2.2**_(continued)_||**Examples**<br>Tools and techniques can facilitate both<br>management and security of these types of<br>accounts and confirm individual user identity<br>before access to an account is granted. Entities<br>can consider password vaults or other system-<br>managed controls such as the_sudo_command.<br>An example of an exceptional circumstance is<br>where all other authentication methods have<br>failed, and a shared ID is needed for emergency<br>use or “break the glass” administrator access.|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**8.2.3** **_Additional requirement for service_**<br>**_providers only:_**Service providers with remote<br>access to customer premises use unique<br>authentication factors for each customer premises.<br>**Customized Approach Objective**<br>A service provider’s credential used for one<br>customer cannot be used for any other customer.|**8.2.3** **_Additional testing procedure for service_**<br>**_provider assessments only:_**Examine<br>authentication policies and procedures and<br>interview personnel to verify that service providers<br>with remote access to customer premises use<br>unique authentication factors for remote access to<br>each customer premises.|Service providers with remote access to customer<br>premises typically use this access to support POS<br>POI systems or provide other remote services.<br>If a service provider uses the same authentication<br>factors to access multiple customers, all the<br>service provider’s customers can easily be<br>compromised if an attacker compromises that one<br>factor.<br>Criminals know this and deliberately target<br>service providers looking for a shared<br>authentication factor that gives them remote<br>access to many merchants via that single factor.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 180_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Applicability Notes**|**Examples**|
|---|---|
|This requirement applies only when the entity being|Technologies such as multi-factor mechanisms<br>that provide a unique credential for each|
|assessed is a service provider.|connection (such as a single-use password) could|
|This requirement is not intended to apply to service|also meet the intent of this requirement.|
|providers accessing their own shared services<br>environments, where multiple customer<br>environments are hosted.||
|If service provider employees use shared<br>authentication factors to remotely access customer<br>premises, these factors must be unique per||
|customer and managed in accordance with<br>Requirement 8.2.2.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 181_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**8.2.4**Addition, deletion, and modification of user<br>IDs, authentication factors, and other identifier<br>objects are managed as follows:<br>•<br>Authorized with the appropriate approval.<br>•<br>Implemented with only the privileges specified<br>on the documented approval.<br>**Customized Approach Objective**|**8.2.4**Examine documented authorizations across<br>various phases of the account lifecycle (additions,<br>modifications, and deletions) and examine system<br>settings to verify the activity has been managed in<br>accordance with all elements specified in this<br>requirement.|It is imperative that the lifecycle of a user ID<br>(additions, deletions, and modifications) is<br>controlled so that only authorized accounts can<br>perform functions, actions are auditable, and<br>privileges are limited to only what is required.<br>Attackers often compromise an existing account<br>and then escalate the privileges of that account to<br>perform unauthorized acts, or they may create<br>new IDs to continue their activity in the<br>background. It is essential to detect and respond|
|Lifecycle events for user IDs and authentication<br>factors cannot occur without appropriate<br>authorization.||when user IDs are created or changed outside the<br>normal change process or without corresponding<br>authorization.|
|**Applicability Notes**|||
|This requirement applies to all user accounts,<br>including employees, contractors, consultants,<br>temporary workers, and third-party vendors.|||
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**8.2.5**Access for terminated users is immediately<br>revoked.|**8.2.5.a**Examine information sources for terminated<br>users and review current user access lists—for<br>both local and remote access—to verify that<br>terminated user IDs have been deactivated or<br>removed from the access lists.|If an employee or third party/vendor has left the<br>company and still has access to the network via<br>their user account, unnecessary or malicious<br>access to cardholder data could occur—either by<br>the former employee or by a malicious user who<br>exploits the old and/or unused account.|
|**Customized Approach Objective**|**8.2.5.b**Interview responsible personnel to verify<br>that all physical authentication factors—such as,<br>smart cards, tokens, etc.—have been returned or<br>deactivated for terminated users.||



The accounts of terminated users cannot be used. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 182_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**8.2.6**Inactive user accounts are removed or<br>disabled within 90 days of inactivity.|**8.2.6**Examine user accounts and last logon<br>information, and interview personnel to verify that<br>any inactive user accounts are removed or|Accounts that are not used regularly are often<br>targets of attack since it is less likely that any<br>changes, such as a changed password, will be<br>noticed. As such, these accounts may be more|
|**Customized Approach Objective**|disabled within 90 days of inactivity.|<br>easily exploited and used to access cardholder<br>data.|
|Inactive user accounts cannot be used.||**Good Practice**<br>Where it may be reasonably anticipated that an<br>account will not be used for an extended period of<br>time, such as an extended leave of absence, the<br>account should be disabled as soon as the leave<br>begins, rather than waiting 90 days.|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**8.2.7**Accounts used by third parties to access,<br>support, or maintain system components via remote<br>access are managed as follows:<br>•<br>Enabled only during the time period needed and<br>disabled when not in use.<br>•<br>Use is monitored for unexpected activity.|**8.2.7**Interview personnel, examine documentation<br>for managing accounts, and examine evidence to<br>verify that accounts used by third parties for<br>remote access are managed according to all<br>elements specified in this requirement.|Allowing third parties to have 24/7 access into an<br>entity’s systems and networks in case they need<br>to provide support increases the chances of<br>unauthorized access. This access could result in<br>an unauthorized user in the third party’s<br>environment or a malicious individual using the<br>always-available external entry point into an<br>entity’s network. Where third parties do need<br>access 24/7, it should be documented, justified,<br>monitored, and tied to specific service reasons.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 183_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Customized Approach Objective**|**Good Practice**<br>Enabling access only for the time periods needed|
|Third-party remote access cannot be used except|and disabling it as soon as it is no longer required|
|where specifically authorized and use is overseen<br>by management.|helps prevent misuse of these connections.<br>Additionally, consider assigning third parties a<br>start and stop date for their access in accordance<br>with their service contract.|
||Monitoring third-party access helps ensure that<br>third parties are accessing only the systems<br>necessary and only during approved time frames.<br>Any unusual activity using third-party accounts<br>should be followed up and resolved.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 184_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**8.2.8**If a user session has been idle for more than<br>15 minutes, the user is required to re-authenticate to<br>re-activate the terminal or session.|**8.2.8**Examine system configuration settings to<br>verify that system/session idle timeout features for<br>user sessions have been set to 15 minutes or less.|When users walk away from an open machine<br>with access to system components or cardholder<br>data, there is a risk that the machine may be used<br>by others in the user’s absence, resulting in|
|**Customized Approach Objective**||unauthorized account access and/or misuse.<br>**Good Practice**|
|A user session cannot be used except by the<br>authorized user.||The re-authentication can be applied either at the<br>system level to protect all sessions running on<br>that machine or at the application level.|
|**Applicability Notes**||Entities may also want to consider staging<br>controls in succession to further restrict the|
|This requirement is not intended to apply to user<br>accounts on point-of-sale terminals that have<br>access to only one card number at a time to<br>facilitate a single transaction.||access of an unattended session as time passes.<br>For example, the screensaver may activate after<br>15 minutes and log off the user after an hour.<br>However, timeout controls must balance the risk|
|This requirement is not meant to prevent legitimate<br>activities from being performed while the<br>console/PC is unattended.||of access and exposure with the impact to the<br>user and purpose of the access.<br>If a user needs to run a program from an<br>unattended computer, the user can log in to the<br>computer to initiate the program, and then “lock”<br>the computer so that no one else can use the<br>user’s login while the computer is unattended.<br>**Examples**<br>One way to meet this requirement is to configure<br>an automated screensaver to launch whenever<br>the console is idle for 15 minutes and requiring<br>the logged-in user to enter their password to<br>unlock the screen.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 185_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **8.3 Strong authentication for users and administrators is established and managed.** 

**Defined Approach Requirements Defined Approach Testing Procedures Purpose** When used in addition to unique IDs, an **8.3.1** All user access to system components for **8.3.1.a** Examine documentation describing the authentication factor helps protect user IDs from users and administrators is authenticated via at authentication factor(s) used to verify that user being compromised, since the attacker needs to least one of the following authentication factors: access to system components is authenticated via have the unique ID and compromise the • Something you know, such as a password or at least one authentication factor specified in this associated authentication factor(s). passphrase. requirement. **Good Practice** • Something you have, such as a token device or **8.3.1.b** For each type of authentication factor used A common approach for a malicious individual to smart card. with each type of system component, observe an compromise a system is to exploit weak or • Something you are, such as a biometric authentication to verify that authentication is nonexistent authentication factors (for example, element. functioning consistently with documented passwords/passphrases). Requiring strong authentication factor(s). authentication factors helps protect against this **Customized Approach Objective** attack. 

###### **Customized Approach Objective** 

###### **Further Information** 

An account cannot be accessed except with a combination of user identity and an authentication factor. 

See _fidoalliance.org_ for more information about using tokens, smart cards, or biometrics as authentication factors. 

###### **Applicability Notes** 

This requirement is not intended to apply to user accounts on point-of-sale terminals that have access to only one card number at a time to facilitate a single transaction. This requirement does not supersede multi-factor authentication (MFA) requirements but applies to those in-scope systems not otherwise subject to MFA requirements. A digital certificate is a valid option for “something you have” if it is unique for a particular user. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 186_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**8.3.2**Strong cryptography is used to render all<br>authentication factors unreadable during<br>transmission and storage on all system<br>components.|**8.3.2.a**Examine vendor documentation and<br>system configuration settings to verify that<br>authentication factors are rendered unreadable<br>with strong cryptography during transmission and<br>storage.|Network devices and applications have been<br>known to transmit unencrypted, readable<br>authentication factors (such as passwords and<br>passphrases) across the network and/or store<br>these values without encryption. As a result, a<br>malicious individual can easily intercept this<br>“”|
||**8.3.2.b**Examine repositories of authentication<br>factors to verify that they are unreadable during<br>storage.|information during transmission using a sniffer,<br>or directly access unencrypted authentication<br>factors in files where they are stored, and then<br>use this data to gain unauthorized access.|
||**8.3.2.c**Examine data transmissions to verify that<br>authentication factors are unreadable during||
|**Customized Approach Objective**|transmission.||
|Cleartext authentication factors cannot be obtained,<br>derived, or reused from the interception of<br>communications or from stored data.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 187_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**8.3.3**User identity is verified before modifying any<br>authentication factor.<br>**Customized Approach Objective**<br>Unauthorized individuals cannot gain system access<br>by impersonating the identity of an authorized user.|**8.3.3**Examine procedures for modifying<br>authentication factors and observe security<br>personnel to verify that when a user requests a<br>modification of an authentication factor, the user’s<br>identity is verified before the authentication factor<br>is modified.|Malicious individuals use "social engineering”<br>techniques to impersonate a user of a system —<br>for example, calling a help desk and acting as a<br>legitimate user—to have an authentication factor<br>changed so they can use a valid user ID.<br>Requiring positive identification of a user reduces<br>the probability of this type of attack succeeding.<br>**Good Practice**<br>Modifications to authentication factors for which<br>user identity should be verified include but are not<br>limited to performing password resets,<br>provisioning new hardware or software tokens,<br>and generating new keys.<br>**Examples**<br>Methods to verify a user’s identity include a secret<br>question/answer, knowledge-based information,<br>and calling the user back at a known and<br>previously established phone number.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 188_ 



###### **Requirements and Testing Procedures** 

###### **Defined Approach Requirements** 

###### **Defined Approach Testing Procedures** 

**8.3.4** Invalid authentication attempts are limited by: **8.3.4.a** Examine system configuration settings to • Locking out the user ID after not more than 10 verify that authentication parameters are set to attempts. require that user accounts be locked out after not more than 10 invalid logon attempts. • Setting the lockout duration to a minimum of 30 minutes or until the user’s identity is confirmed. **8.3.4.b** Examine system configuration settings to verify that password parameters are set to require **Customized Approach Objective** that once a user account is locked out, it remains locked for a minimum of 30 minutes or until the An authentication factor cannot be guessed in a user’s identity is confirmed. 

An authentication factor cannot be guessed in a brute force, online attack. 

###### **Guidance** 

###### **Purpose** 

Without account-lockout mechanisms in place, an attacker can continually try to guess a password through manual or automated tools (for example, password cracking) until the attacker succeeds and gains access to a user’s account. 

If an account is locked out due to someone continually trying to guess a password, controls to delay reactivation of the locked account stop the malicious individual from guessing the password, as they will have to stop for a minimum of 30 minutes until the account is reactivated. 

###### **Good Practice** 

###### **Applicability Notes** 

This requirement is not intended to apply to user accounts on point-of-sale terminals that have access to only one card number at a time to facilitate a single transaction. 

###### **Defined Approach Requirements** 

###### **Defined Approach Testing Procedures** 

- **8.3.5** If passwords/passphrases are used as **8.3.5** Examine procedures for setting and resetting authentication factors to meet Requirement 8.3.1, passwords/passphrases (if used as authentication they are set and reset for each user as follows: factors to meet Requirement 8.3.1) and observe • Set to a unique value for first-time use and upon security personnel to verify that reset. passwords/passphrases are set and reset in accordance with all elements specified in this 

- • Forced to be changed immediately after the first requirement. 

- use. 

Before reactivating a locked account, the user’s identity should be confirmed. For example, the administrator or help desk personnel can validate that the actual account owner is requesting reactivation, or there may be password reset selfservice mechanisms that the account owner uses to verify their identity. 

###### **Purpose** 

If the same password/passphrase is used for every new user, an internal user, former employee, or malicious individual may know or easily discover the value and use it to gain access to accounts before the authorized user attempts to use the password. 

###### **Customized Approach Objective** 

An initial or reset password/passphrase assigned to a user cannot be used by an unauthorized user. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 189_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**8.3.6**If passwords/passphrases are used as<br>authentication factors to meet Requirement 8.3.1,<br>they meet the following minimum level of<br>complexity:<br>•<br>A minimum length of 12 characters (or IF the<br>system does not support 12 characters, a<br>minimum length of eight characters).|**8.3.6**Examine system configuration settings to<br>verify that user password/passphrase complexity<br>parameters are set in accordance with all elements<br>specified in this requirement.|Strong passwords/passphrases may be the first<br>line of defense into a network since a malicious<br>individual will often first try to find accounts with<br>weak, static, or non-existent passwords. If<br>passwords are short or easily guessable, it is<br>relatively easy for a malicious individual to find<br>these weak accounts and compromise a network<br>under the guise of a valid user ID.|
|•<br>Contain both numeric and alphabetic characters.||**Good Practice**|
|**Customized Approach Objective**<br>A guessed password/passphrase cannot be verified<br>by either an online or offline brute force attack.<br>**Applicability Notes**<br>This requirement is not intended to apply to:<br>•<br>User accounts on point-of-sale terminals that<br>have access to only one card number at a time<br>to facilitate a single transaction.||Password/passphrase strength is dependent on<br>password/passphrase complexity, length, and<br>randomness. Passwords/passphrases should be<br>sufficiently complex, so they are impractical for an<br>attacker to guess or otherwise discover its value.<br>Entities can consider adding increased complexity<br>by requiring the use of special characters and<br>upper- and lower-case characters, in addition to<br>the minimum standards outlined by this<br>requirement. Additional complexity increases the<br>time required for offline brute force attacks of<br>hashed passwords/passphrases.|
|•<br>Application or system accounts, which are<br>governed by requirements in section 8.6.<br>_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._<br>Until 31 March 2025, passwords must be a<br>minimum length of seven characters in accordance<br>with PCI DSS v3.2.1 Requirement 8.2.3.||Another option for increasing the resistance of<br>passwords to guessing attacks is by comparing<br>proposed password/passphrases to a bad<br>password list and having users provide new<br>passwords for any passwords found on the list.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 190_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**8.3.7**Individuals are not allowed to submit a new<br>password/passphrase that is the same as any of the<br>last four passwords/passphrases used.<br>**Customized Approach Objective**|**8.3.7**Examine system configuration settings to<br>verify that password parameters are set to require<br>that new passwords/passphrases cannot be the<br>same as the four previously used<br>passwords/passphrases.|If password history is not maintained, the<br>effectiveness of changing passwords is reduced,<br>as previous passwords can be reused over and<br>over. Requiring that passwords cannot be reused<br>for a period reduces the likelihood that passwords<br>that have been guessed or brute-forced will be re-|
|A previously used password cannot be used to gain<br>access to an account for at least 12 months.||used in the future.<br>Passwords or passphrases may have previously<br>been changed due to suspicion of compromise or|
|**Applicability Notes**||because the password or passphrase exceeded<br>its effective use period, both of which are reasons|
|This requirement is not intended to apply to user<br>accounts on point-of-sale terminals that have<br>access to only one card number at a time to||why previously used passwords should not be<br>reused.|
|facilitate a single transaction.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 191_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**8.3.8**Authentication policies and procedures are<br>documented and communicated to all users<br>including:<br><br>|**8.3.8.a**Examine procedures and interview<br>personnel to verify that authentication policies and<br>procedures are distributed to all users.|Communicating authentication policies and<br>procedures to all users helps them to understand<br>and abide by the policies.<br>**Good Practice**|
|•<br>Guidance on selecting strong authentication<br>factors.<br>•<br>Guidance for how users should protect their<br>authentication factors.<br>•<br>Instructions not to reuse previously used|**8.3.8.b**Review authentication policies and<br>procedures that are distributed to users and verify<br>they include the elements specified in this<br>requirement.|Guidance on selecting strong passwords may<br>include suggestions to help personnel select<br>hard-to-guess passwords that do not contain<br>dictionary words or information about the user,<br>such as the user ID, names of family members,|
|passwords/passphrases.|**8.3.8.c**Interview users to verify that they are|date of birth, etc.|
|•<br>Instructions to change passwords/passphrases if<br>there is any suspicion or knowledge that the<br>password/passphrases have been compromised<br>and how to report the incident.|familiar with authentication policies and<br>procedures.|Guidance for protecting authentication factors<br>may include not writing down passwords or not<br>saving them in insecure files, and being alert to<br>malicious individuals who may try to exploit their<br>passwords (for example, by calling an employee|
|**Customized Approach Objective**||and asking for their password so the caller can<br>“troubleshoot a problem”).|
|Users are knowledgeable about the correct use of<br>authentication factors and can access assistance<br>and guidance when required.||Alternatively, entities can implement processes to<br>confirm passwords meet password policy, for<br>example, by comparing password choices to a list<br>of unacceptable passwords and having users<br>choose a new password for any that match with<br>one on the list. Instructing users to change<br>passwords if there is a chance the password is no<br>longer secure can prevent malicious users from<br>using a legitimate password to gain unauthorized<br>access.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 192_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**8.3.9**If passwords/passphrases are used as the<br>only authentication factor for user access (i.e., in<br>any single-factor authentication implementation)<br>then either:<br>•<br>Passwords/passphrases are changed at least<br>once every 90 days,<br>**OR**<br>•<br>The security posture of accounts is dynamically<br>analyzed, and real-time access to resources is<br>automatically determined accordingly.|**8.3.9**If passwords/passphrases are used as the<br>only authentication factor for user access, inspect<br>system configuration settings to verify that<br>passwords/passphrases are managed in<br>accordance with ONE of the elements specified in<br>this requirement.|Access to in-scope system components that are<br>not in the CDE may be provided using a single<br>authentication factor, such as a<br>password/passphrase, token device or smart<br>card, or biometric attribute. Where<br>passwords/passphrases are employed as the only<br>authentication factor for such access, additional<br>controls are required to protect the integrity of the<br>password/passphrase.<br>**Good Practice**<br>Passwords/passphrases that are valid for a long<br>time without a change provide malicious|
|**Customized Approach Objective**<br>An undetected compromised password/passphrase<br>cannot be used indefinitely.<br>**Applicability Notes**<br>This requirement does not apply to in-scope system<br>components where MFA is used.<br>This requirement is not intended to apply to user<br>accounts on point-of-sale terminals that have<br>access to only one card number at a time to<br>facilitate a single transaction.<br>This requirement does not apply to service<br>providers’ customer accounts but does apply to<br>accounts for service provider personnel.||individuals with more time to break the<br>password/phrase. Periodically changing<br>passwords offers less time for a malicious<br>individual to crack a password/passphrase and<br>less time to use a compromised password.<br>Using a password/passphrase as the only<br>authentication factor provides a single point of<br>failure if compromised. Therefore, in these<br>implementations, controls are needed to minimize<br>how long malicious activity could occur via a<br>compromised password/passphrase.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 193_ 



||**Requirements and Testing Procedures**|**Guidance**|
|---|---|---|
|**8.3.9**_(continued)_||Dynamically analyzing an account’s security<br>posture is another option that allows for more<br>rapid detection and response to address<br>potentially compromised credentials. Such<br>analysis takes a number of data points, which<br>may include device integrity, location, access<br>times, and the resources accessed to determine<br>in real time whether an account can be granted<br>access to a requested resource. In this way,<br>access can be denied and accounts blocked if it is<br>suspected that authentication credentials have<br>been compromised.<br>**Further Information**<br>For information about using dynamic analysis to<br>manage user access to resources, see_NIST SP_<br>_800-207 Zero Trust Architecture_.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 194_ 



###### **Requirements and Testing Procedures** 

**Defined Approach Requirements Defined Approach Testing Procedures 8.3.10** **_Additional requirement for service_ 8.3.10** **_Additional testing procedure for service providers only:_** If passwords/passphrases are **_provider assessments only:_** If used as the only authentication factor for customer passwords/passphrases are used as the only user access to cardholder data (i.e., in any singleauthentication factor for customer user access to factor authentication implementation), then cardholder data, examine guidance provided to guidance is provided to customer users including: customer users to verify that the guidance includes • Guidance for customers to change their user all elements specified in this requirement. 

- Guidance for customers to change their user passwords/passphrases periodically. 

- Guidance as to when, and under what circumstances, passwords/passphrases are to be changed. 

###### **Customized Approach Objective** 

###### **Guidance** 

###### **Purpose** 

Using a password/passphrase as the only authentication factor provides a single point of failure if compromised. Therefore, in these implementations, controls are needed to minimize how long malicious activity could occur via a compromised password/passphrase. 

###### **Good Practice** 

Passwords/passphrases that are valid for a long time without a change provide malicious individuals with more time to break the password/phrase. Periodically changing passwords offers less time for a malicious individual to crack a password/passphrase and less time to use a compromised password. 

Passwords/passphrases for service providers’ customers cannot be used indefinitely. 

###### **Applicability Notes** 

This requirement applies only when the entity being assessed is a service provider. This requirement does not apply to accounts of consumer users accessing their own payment card information. _This requirement for service providers will be superseded by Requirement 8.3.10.1 once 8.3.10.1 becomes effective._ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 195_ 



###### **Requirements and Testing Procedures** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|
|---|---|
|**8.3.10.1****_Additional requirement for service_**<br>**_providers only:_** If passwords/passphrases are<br>used as the only authentication factor for customer<br>user access (i.e., in any single-factor authentication<br>implementation) then either:<br>•<br>Passwords/passphrases are changed at least<br>once every 90 days,<br>**OR**|**8.3.10.1****_Additional testing procedure for_**<br>**_service provider assessments only:_**If<br>passwords/passphrases are used as the only<br>authentication factor for customer user access,<br>inspect system configuration settings to verify that<br>passwords/passphrases are managed in<br>accordance with ONE of the elements specified in<br>this requirement.|



- The security posture of accounts is dynamically analyzed, and real-time access to resources is automatically determined accordingly. 

###### **Customized Approach Objective** 

Passwords/passphrases for service providers’ customers cannot be used indefinitely. **Applicability Notes** This requirement applies only when the entity being assessed is a service provider. This requirement does not apply to accounts of consumer users accessing their own payment card information. _This requirement is a best practice until 31 March 2025, after which it will be required and must be fully considered during a PCI DSS assessment._ Until this requirement is effective on 31 March 2025, service providers may meet either Requirement 8.3.10 or 8.3.10.1. 

###### **Guidance** 

###### **Purpose** 

Using a password/passphrase as the only authentication factor provides a single point of failure if compromised. Therefore, in these implementations, controls are needed to minimize how long malicious activity could occur via a compromised password/passphrase. **Good Practice** 

Passwords/passphrases that are valid for a long time without a change provide malicious individuals with more time to break the password/phrase. Periodically changing passwords offers less time for a malicious individual to crack a password/passphrase and less time to use a compromised password. Dynamically analyzing an account’s security posture is another option that allows for more rapid detection and response to address potentially compromised credentials. Such analysis takes a number of data points which may include device integrity, location, access times, and the resources accessed to determine in real time whether an account can be granted access to a requested resource. In this way, access can be denied and accounts blocked if it is suspected that account credentials have been compromised. 

###### **Further Information** 

For information about using dynamic analysis to manage user access to resources, refer to _NIST SP 800-207 Zero Trust Architecture_ . 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 196_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**8.3.11**Where authentication factors such as<br>physical or logical security tokens, smart cards, or<br>certificates are used:<br>•<br>Factors are assigned to an individual user and<br>not shared among multiple users.<br>•<br>Physical and/or logical controls ensure only the<br>|**8.3.11.a**Examine authentication policies and<br>procedures to verify that procedures for using<br>authentication factors such as physical security<br>tokens, smart cards, and certificates are defined<br>and include all elements specified in this<br>requirement.|If multiple users can use authentication factors<br>such as tokens, smart cards, and certificates, it<br>may be impossible to identify the individual using<br>the authentication mechanism.<br>**Good Practice**<br>Having physical and/or logical controls (for<br>example, a PIN, biometric data, or a password) to|
|intended user can use that factor to gain access.|**8.3.11.b**Interview security personnel to verify<br>authentication factors are assigned to an individual<br>user and not shared among multiple users.|uniquely authenticate the user of the account will<br>prevent unauthorized users from gaining access<br>to the user account through use of a shared<br>authentication factor.|
|**Customized Approach Objective**<br>An authentication factor cannot be used by anyone<br>other than the user to which it is assigned.|**8.3.11.c**Examine system configuration settings<br>and/or observe physical controls, as applicable, to<br>verify that controls are implemented to ensure only<br>the intended user can use that factor to gain<br>access.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 197_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **8.4 Multi-factor authentication (MFA) is implemented to secure access into the CDE.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**8.4.1**MFA is implemented for all non-console<br>access into the CDE for personnel with<br>administrative access.|**8.4.1.a**Examine network and/or system<br>configurations to verify MFA is required for all non-<br>console into the CDE for personnel with<br>administrative access.|Requiring more than one type of authentication<br>factor reduces the probability that an attacker can<br>gain access to a system by masquerading as a<br>legitimate user, because the attacker would need<br>to compromise multiple authentication factors.|
|**Customized Approach Objective**|**8.4.1.b**Observe administrator personnel logging<br>into the CDE and verify that MFA is required.|This is especially true in environments where<br>traditionally the single authentication factor<br>employed was something a user knows such as a<br>password or passphrase.|
|Administrative access to the CDE cannot be<br>obtained by the use of a single authentication factor.||**Good Practice**<br>Implementing MFA for non-console administrative<br>access to in-scope system components that are|
|**Applicability Notes**||not part of the CDE will help prevent unauthorized<br>users from using a single factor to gain access|
|The requirement for MFA for non-console||and compromise in-scope system components.|
|administrative access applies to all personnel with<br>elevated or increased privileges accessing the CDE<br>via a non-console connection—that is, via logical<br>access occurring over a network interface rather<br>than via a direct, physical connection.||**Definitions**<br>Using one factor twice (for example, using two<br>separate passwords) is not considered multi-<br>factor authentication.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 198_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**8.4.2**MFA is implemented for all non-console<br>access into the CDE.|**8.4.2.a**Examine network and/or system<br>configurations to verify MFA is implemented for all<br>non-console access into the CDE.|Requiring more than one type of authentication<br>factor reduces the probability that an attacker can<br>gain access to a system by masquerading as a<br>legitimate user, because the attacker would need|
|**Customized Approach Objective**|**8.4.2.b**Observe personnel logging in to the CDE<br>and examine evidence to verify that MFA is<br>required.|to compromise multiple authentication factors.<br>This is especially true in environments where<br>traditionally the single authentication factor<br>employed was something a user knows such as a|
|Access into the CDE cannot be obtained by the use<br>of a single authentication factor.||password or passphrase.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 199_ 



###### **Requirements and Testing Procedures Guidance** 

|**Applicability Notes**|**Definitions**|
|---|---|
|This requirement does not apply to:<br>•<br>Application or system accounts performing<br>automated functions.|Using one factor twice (for example, using two<br>separate passwords) is not considered multi-<br>factor authentication.<br>Refer to_Appendix G_for the definition of “phishing|
|•<br>User accounts on point-of-sale terminals that<br>have access to only one card number at a time<br>to facilitate a single transaction.|resistant authentication.”|
|•<br>User accounts that are only authenticated with<br>phishing-resistant authentication factors.||
|MFA is required for both types of access specified in||
|Requirements 8.4.2 and 8.4.3. Therefore, applying<br>MFA to one type of access does not replace the<br>need to apply another instance of MFA to the other<br>type of access. If an individual first connects to the<br>entity’s network via remote access, and then later<br>initiates a connection into the CDE from within the<br>network, per this requirement the individual would<br>authenticate using MFA twice, once when<br>connecting via remote access to the entity’s network<br>and once when connecting from the entity’s network<br>into the CDE.||
|_(continued on next page)_||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 200_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|The MFA requirements apply for all types of system<br>components, including cloud, hosted systems, and<br>on-premises applications, network security devices,<br>workstations, servers, and endpoints, and includes<br>access directly to an entity’s networks or systems as<br>well as web-based access to an application or<br>function.||
|MFA for access into the CDE can be implemented<br>at the network or system/application level; it does<br>not have to be applied at both levels. For example, if<br>MFA is used when a user connects to the CDE<br>network, it does not have to be used when the user<br>logs into each system or application within the CDE.||
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 201_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**8.4.3**MFA is implemented for all remote access<br>originating from outside the entity’s network that<br>could access or impact the CDE.|**8.4.3.a**Examine network and/or system<br>configurations for remote access servers and<br>systems to verify MFA is required in accordance<br>with all elements specified in this requirement.|Requiring more than one type of authentication<br>factor reduces the probability that an attacker can<br>gain access to a system by masquerading as a<br>legitimate user, because the attacker would need<br>to compromise multiple authentication factors.|
||**8.4.3.b**Observe personnel (for example, users and<br>administrators) and third parties connecting<br>remotely to the network and verify that multi-factor<br>thtiti i id|This is especially true in environments where<br>traditionally the single authentication factor<br>employed was something a user knows, such as<br>a password or passphrase.|
|**Customized Approach Objective**|auencaon s requre.|**Definitions**<br>Multi-factor authentication (MFA) requires an|
|Remote access to the entity’s network cannot be<br>obtained by using a single authentication factor.||individual to present a minimum of two of the<br>three authentication factors specified in<br>Requirement 8.3.1 before access is granted.<br>Using one factor twice (for example, using two<br>separate passwords) is not considered multi-<br>factor authentication.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 202_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Applicability Notes**||
|The requirement for MFA for remote access<br>originating from outside the entity’s network applies<br>to all user accounts that can access the network<br>remotely, where that remote access leads to or<br>could lead to access into the CDE. This includes all<br>remote access by personnel (users and<br>administrators), and third parties (including, but not<br>limited to, vendors, suppliers, service providers, and<br>customers).<br>If remote access is to a part of the entity’s network<br>that is properly segmented from the CDE, such that<br>remote users cannot access or impact the CDE,<br>MFA for remote access to that part of the network is<br>not required. However, MFA is required for any<br>remote access to networks with access to the CDE<br>and is recommended for all remote access to the<br>entity’s networks.||
|The MFA requirements apply for all types of system<br>components, including cloud, hosted systems, and<br>on-premises applications, network security devices,<br>workstations, servers, and endpoints, and includes<br>access directly to an entity’s networks or systems as<br>well as web-based access to an application or<br>function.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 203_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **8.5 Multi-factor authentication (MFA) systems are configured to prevent misuse.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**8.5.1**MFA systems are implemented as follows:<br>•<br>The MFA system is not susceptible to replay<br>attacks.|**8.5.1.a**Examine vendor system documentation to<br>verify that the MFA system is not susceptible to<br>replay attacks.|Poorly configured MFA systems can be bypassed<br>by attackers. This requirement therefore<br>addresses configuration of MFA system(s) that<br>provide MFA for users accessing system|
|•<br>MFA systems cannot be bypassed by any users,<br>including administrative users unless specifically<br>documented, and authorized by management on<br>an exception basis, for a limited time period.<br>•<br>At least two different types of authentication|**8.5.1.b**Examine system configurations for the<br>MFA implementation to verify it is configured in<br>accordance with all elements specified in this<br>requirement.|components in the CDE.<br>**Definitions**<br>Using one type of factor twice (for example, using<br>two separate passwords) is not considered multi-<br>factor authentication.|
|factors are used.<br>•<br>Success of all authentication factors is required<br>before access is granted.|**8.5.1.c**Interview responsible personnel and<br>observe processes to verify that any requests to<br>bypass MFA are specifically documented and<br>authorized by management on an exception basis,<br>for a limited time period.|A replay attack is when an attacker intercepts a<br>valid transmission of data and then resends or<br>redirects this communication for malicious<br>purposes. In MFA implementations, replay attacks<br>are typically used to gain unauthorized access by<br>leveraging legitimate credentials.|
||**8.5.1.d**Observe personnel logging into system<br>components in the CDE to verify that access is<br>granted only after all authentication factors are<br>successful.|**Examples**<br>Examples of methods to help protect against<br>replay attacks include, but are not limited to:<br>•<br>Unique session identifiers and session keys|
||**8.5.1.e**Observe personnel connecting remotely|•<br>Timestamps|
|**Customized Approach Objective**<br>MFA systems are resistant to attack and strictly<br>control any administrative overrides.|from outside the entity’s network to verify that<br>access is granted only after all authentication<br>factors are successful.|•<br>Time-based, one-time passwords or<br>passcodes<br>•<br>Anti-replay mechanisms that detect and reject<br>duplicated authentication attempts.|
|||_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 204_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Applicability Notes**<br>_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._|**Further Information**<br>For more information about MFA systems and<br>features, refer to the following:<br>PCI SSC’s_Information Supplement: Multi-Factor_<br>_Authentication_|
||PCI SSC’s Frequently Asked Questions (FAQs)<br>on this topic.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 205_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **8.6 Use of application and system accounts and associated authentication factors is strictly managed.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**8.6.1**If accounts used by systems or applications<br>can be used for interactive login, they are managed<br>as follows:<br>•<br>Interactive use is prevented unless needed for<br>an exceptional circumstance.|**8.6.1**Examine application and system accounts<br>that can be used interactively and interview<br>administrative personnel to verify that application<br>and system accounts are managed in accordance<br>with all elements specified in this requirement.|Like individual user accounts, system and<br>application accounts require accountability and<br>strict management to ensure they are used only<br>for the intended purpose and are not misused.<br>Attackers often compromise system or application<br>accounts to gain access to cardholder data.|
|•<br>Interactive use is limited to the time needed for<br>the exceptional circumstance.<br>•<br>Business justification for interactive use is<br>documented.||**Good Practice**<br>Where possible, configure system and application<br>accounts to disallow interactive login to prevent<br>unauthorized individuals from logging in and using|
|•<br>Interactive use is explicitly approved by<br>management.||the account with its associated system privileges,<br>and to limit the machines and devices on which|
|•<br>Individual user identity is confirmed before<br>access to account is granted.||the account can be used.<br>**Definitions**|
|•<br>Every action taken is attributable to an individual<br>user.||Interactive login is the ability for a person to log<br>into a system or application account in the same|
|**Customized Approach Objective**||manner as a normal user account. Using system<br>and application accounts this way means there is<br>no accountability and traceability of actions taken|
|When used interactively, all actions with accounts||by the user.|
|designated as system or application accounts are<br>authorized and attributable to an individual person.||Refer to_Appendix G_for the definition of<br>“application and system accounts.”|



###### **Applicability Notes** 

_This requirement is a best practice until 31 March 2025, after which it will be required and must be fully considered during a PCI DSS assessment._ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 206_ 



###### **Requirements and Testing Procedures** 

**Defined Approach Requirements Defined Approach Testing Procedures 8.6.2** Passwords/passphrases for any application **8.6.2.a** Interview personnel and examine system and system accounts that can be used for development procedures to verify that processes interactive login are not hard coded in scripts, are defined for application and system accounts configuration/property files, or bespoke and custom that can be used for interactive login, specifying source code. that passwords/passphrases are not hard coded in scripts, configuration/property files, or bespoke and custom source code. **8.6.2.b** Examine scripts, configuration/property files, and bespoke and custom source code for **Customized Approach Objective** application and system accounts that can be used for interactive login, to verify Passwords/passphrases used by application and passwords/passphrases for those accounts are not system accounts cannot be used by unauthorized present. personnel. **Applicability Notes** Stored passwords/passphrases are required to be encrypted in accordance with PCI DSS Requirement 8.3.2. _This requirement is a best practice until 31 March 2025, after which it will be required and must be fully considered during a PCI DSS assessment._ 

###### **Guidance** 

###### **Purpose** 

Not properly protecting passwords/passphrases used by application and system accounts, especially if those accounts can be used for interactive login, increases the risk and success of unauthorized use of those privileged accounts. 

**Good Practice** Changing these values due to suspected or confirmed disclosure can be particularly difficult to implement. Tools can facilitate both management and security of authentication factors for application and system accounts. For example, consider password vaults or other system-managed controls. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 207_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**8.6.3**Passwords/passphrases for any application<br>and system accounts are protected against misuse<br>as follows:<br>•<br>Passwords/passphrases are changed<br>periodically (at the frequency defined in the<br>|**8.6.3.a**Examine policies and procedures to verify<br>that procedures are defined to protect<br>passwords/passphrases for application or system<br>accounts against misuse in accordance with all<br>elements specified in this requirement.|Systems and application accounts pose more<br>inherent security risk than user accounts because<br>they often run in an elevated security context, with<br>access to systems that may not be typically<br>granted to user accounts, such as programmatic<br>access to databases, etc. As a result, special|
|entity’s targeted risk analysis, which is<br>performed according to all elements specified in<br>Requirement 12.3.1) and upon suspicion or<br>confirmation of compromise.<br>•<br>Passwords/passphrases are constructed with<br>sufficient complexity appropriate for how<br>frequently the entity changes the<br>passwords/passphrases.|**8.6.3.b**Examine the entity’s targeted risk analysis<br>for the change frequency and complexity for<br>passwords/passphrases for application and system<br>accounts to verify the risk analysis was performed<br>in accordance with all elements specified in<br>Requirement 12.3.1 and addresses:<br>•<br>The frequency defined for periodic changes to<br>application and system<br>passwords/passphrases.<br>•<br>The complexity defined for<br>passwords/passphrases and appropriateness<br>of the complexity relative to the frequency of<br>changes.|consideration must be made to protect<br>passwords/passphrases used for application and<br>system accounts.<br>**Good Practice**<br>Entities should consider the following risk factors<br>when determining how to protect application and<br>system passwords/passphrases against misuse:<br>•<br>How securely the passwords/passphrases are<br>stored (for example, whether they are stored<br>in a password vault).<br>•<br>Staff turnover.<br>•<br>The number of people with access to the<br>authentication factor.|
|**Customized Approach Objective**<br>Passwords/passphrases used by application and<br>system accounts cannot be used indefinitely and<br>are structured to resist brute-force and guessing<br>k|**8.6.3.c**Interview responsible personnel and<br>examine system configuration settings to verify that<br>passwords/passphrases for any application and<br>system accounts are protected against misuse in<br>accordance with all elements specified in this<br>|•<br>Whether the account can be used for<br>interactive login.<br>•<br>Whether the security posture of accounts is<br>dynamically analyzed, and real-time access to<br>resources is automatically determined<br>accordingly (see Requirement 8.3.9).|



• The complexity defined for passwords/passphrases and appropriateness of the complexity relative to the frequency of changes. **Customized Approach Objective 8.6.3.c** Interview responsible personnel and examine system configuration settings to verify that Passwords/passphrases used by application and passwords/passphrases for any application and system accounts cannot be used indefinitely and system accounts are protected against misuse in are structured to resist brute-force and guessing accordance with all elements specified in this attacks. requirement. 

All these elements affect the level of risk for application and system accounts and might impact the security of systems accessed by the system and application accounts. _(continued on next page)_ 

###### **Applicability Notes** 

_This requirement is a best practice until 31 March 2025, after which it will be required and must be fully considered during a PCI DSS assessment._ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 208_ 



||**Requirements and Testing Procedures**|**Guidance**|
|---|---|---|
|**8.6.3**_(continued)_||Entities should correlate their selected change<br>frequency for application and system<br>passwords/passwords with their selected<br>complexity for those passwords/passphrases –<br>i.e., the complexity should be more rigorous when<br>passwords/passphrases are changed infrequently<br>and can be less rigorous when changed more<br>frequently. For example, a longer change<br>frequency is more justifiable when<br>passwords/passphrases complexity is set to 36<br>alphanumeric characters with upper- and lower-<br>case letters, numbers, and special characters.<br>Best practices are to consider password changes<br>at least once a year, a password/passphrase<br>length of at least 15 characters, and complexity<br>for the passwords/passphrase of alphanumeric<br>characters, with upper- and lower-case letters,<br>and special characters.|
|||**Further Information**<br>For information about variability and equivalency<br>of password strength for passwords/passphrases<br>of different formats, see the industry standards<br>(for example, the current version of_NIST SP 800-_<br>_63 Digital Identity Guidelines_).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 209_ 



#### **_Requirement 9: Restrict Physical Access to Cardholder Data_** 

**Sections** 

- **9.1** Processes and mechanisms for restricting physical access to cardholder data are defined and understood. 

- **9.2** Physical access controls manage entry into facilities and systems containing cardholder data. 

- **9.3** Physical access for personnel and visitors is authorized and managed. 

- **9.4** Media with cardholder data is securely stored, accessed, distributed, and destroyed. 

- **9.5** Point of interaction (POI) devices are protected from tampering and unauthorized substitution. 

**Overview** 

Any physical access to cardholder data or systems that store, process, or transmit cardholder data provides the opportunity for individuals to access and/or remove systems or hardcopies containing cardholder data; therefore, physical access should be appropriately restricted. There are three different areas mentioned in Requirement 9: 

1. Requirements that specifically refer to sensitive areas are intended to apply to those areas only. Each entity should identify the sensitive areas in its environments to ensure the appropriate physical controls are implemented. 

2. Requirements that specifically refer to the cardholder data environment (CDE) are intended to apply to the entire CDE, including any sensitive areas residing within the CDE. 

3. Requirements that specifically refer to the facility are referencing the types of controls that may be managed more broadly at the physical boundary of a business premise (such as a building) within which CDEs and sensitive areas reside. These controls often exist outside a CDE or sensitive area, for example a guard desk that identifies, badges, and logs visitors. The term “facility” is used to recognize that these controls may exist at different places within a facility, for instance, at building entry or at an internal entrance to a data center or office space. 

Refer to _Appendix G_ for definitions of “media,” “personnel,” “sensitive areas,” “visitors,” and other PCI DSS terms. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 210_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **9.1 Processes and mechanisms for restricting physical access to cardholder data are defined and understood.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**9.1.1**All security policies and operational<br>procedures that are identified in Requirement 9 are:<br>•<br>Documented.<br>•<br>Kept up to date.<br>•<br>In use.<br>•<br>Known to all affected parties.|**9.1.1**Examine documentation and interview<br>personnel to verify that security policies and<br>operational procedures identified in Requirement 9<br>are managed in accordance with all elements<br>specified in this requirement.|Requirement 9.1.1 is about effectively managing<br>and maintaining the various policies and<br>procedures specified throughout Requirement 9.<br>While it is important to define the specific policies<br>or procedures called out in Requirement 9, it is<br>equally important to ensure they are properly<br>documented, maintained, and disseminated.<br>**Good Practice**|
|**Customized Approach Objective**<br>Expectations, controls, and oversight for meeting<br>activities within Requirement 9 are defined and<br>adhered to by affected personnel. All supporting<br>activities are repeatable, consistently applied, and<br>conform to management’s intent.||It is important to update policies and procedures<br>as needed to address changes in processes,<br>technologies, and business objectives. For this<br>reason, consider updating these documents as<br>soon as possible after a change occurs and not<br>only on a periodic cycle.<br>**Definitions**<br>Security policies define the entity’s security<br>objectives and principles. Operational procedures<br>describe how to perform activities, and define the<br>controls, methods, and processes that are<br>followed to achieve the desired result in a<br>consistent manner and in accordance with policy<br>objectives.<br>Policies and procedures, including updates, are<br>actively communicated to all affected personnel,<br>and are supported by operating procedures<br>describing how to perform activities.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 211_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**9.1.2**Roles and responsibilities for performing<br>activities in Requirement 9 are documented,<br>assigned, and understood.|**9.1.2.a**Examine documentation to verify that<br>descriptions of roles and responsibilities for<br>performing activities in Requirement 9 are<br>documented and assigned.|If roles and responsibilities are not formally<br>assigned, personnel may not be aware of their<br>day-to-day responsibilities, and critical activities<br>may not occur.<br>**Good Practice**|
|**Customized Approach Objective**<br>Day-to-day responsibilities for performing all the<br>activities in Requirement 9 are allocated. Personnel<br>are accountable for successful, continuous<br>operation of these requirements.|**9.1.2.b**Interview personnel with responsibility for<br>performing activities in Requirement 9 to verify that<br>roles and responsibilities are assigned as<br>documented and are understood.|Roles and responsibilities may be documented<br>within policies and procedures or maintained<br>within separate documents.<br>As part of communicating roles and<br>responsibilities, entities can consider having<br>personnel acknowledge their acceptance and<br>understanding of their assigned roles and<br>responsibilities.<br>A method to document roles and responsibilities<br>is a responsibility assignment matrix that includes<br>who is responsible, accountable, consulted, and<br>informed (also called a RACI matrix).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 212_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **9.2 Physical access controls manage entry into facilities and systems containing cardholder data.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**9.2.1**Appropriate facility entry controls are in place<br>to restrict physical access to systems in the CDE.|**9.2.1**Observe entry controls and interview<br>responsible personnel to verify that physical<br>security controls are in place to restrict access to<br>systems in the CDE.|Without physical access controls, unauthorized<br>persons could potentially gain access to the CDE<br>and sensitive information, or could alter system<br>configurations, introduce vulnerabilities into the<br>network, or destroy or steal equipment. Therefore,|
|**Customized Approach Objective**||the purpose of this requirement is that physical<br>access to the CDE is controlled via physical|
|System components in the CDE cannot be<br>physically accessed by unauthorized personnel.||security controls such as badge readers or other<br>mechanisms such as lock and key.<br>**Good Practice**|
|**Applicability Notes**<br>This requirement does not apply to locations that<br>are publicly accessible by consumers (cardholders).||Whichever mechanism meets this requirement, it<br>must be sufficient for the organization to verify<br>that only authorized personnel are granted<br>access.<br>**Examples**<br>Facility entry controls include physical security<br>controls at each computer room, data center, and<br>other physical areas with systems in the CDE. It<br>can also include badge readers or other devices<br>that manage physical access controls, such as<br>lock and key with a current list of all individuals<br>holding the keys.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 213_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**9.2.1.1**Individual physical access to sensitive areas<br>within the CDE is monitored with either video<br>cameras or physical access control mechanisms (or<br>both) as follows:<br>•<br>Entry and exit points to/from sensitive areas<br>ithi th CDE  itd|**9.2.1.1.a**Observe locations where individual<br>physical access to sensitive areas within the CDE<br>occurs to verify that either video cameras or<br>physical access control mechanisms (or both) are<br>in place to monitor the entry and exit points.|Maintaining details of individuals entering and<br>exiting the sensitive areas can help with<br>investigations of physical breaches by identifying<br>individuals that physically accessed the sensitive<br>areas, as well as when they entered and exited.<br>**Good Practice**|
|wn e  are monore.<br>•<br>Monitoring devices or mechanisms are protected<br>from tampering or disabling.<br>•<br>Collected data is reviewed and correlated with<br>other entries.|**9.2.1.1.b**Observe locations where individual<br>physical access to sensitive areas within the CDE<br>occurs to verify that either video cameras or<br>physical access control mechanisms (or both) are<br>protected from tampering or disabling.|Whichever mechanism meets this requirement, it<br>should effectively monitor all entry and exit points<br>to sensitive areas.<br>Criminals attempting to gain physical access to<br>sensitive areas will often try to disable or bypass|
|•<br>Collected data is stored for at least three||the monitoring controls. To protect these controls|
|months, unless otherwise restricted by law.|**9.2.1.1.c**Observe the physical access control<br>mechanisms and/or examine video cameras and<br>interview responsible personnel to verify that:|from tampering, video cameras could be<br>positioned so they are out of reach and/or be<br>monitored to detect tampering. Similarly, physical|
|**Customized Approach Objective**<br>Trusted, verifiable records are maintained of<br>individual physical entry to, and exit from, sensitive<br>areas.|•<br>Collected data from video cameras and/or<br>physical access control mechanisms is<br>reviewed and correlated with other entries.<br>•<br>Collected data is stored for at least three<br>months.|access control mechanisms could be monitored<br>or have physical protections installed to prevent<br>them from being damaged or disabled by<br>malicious individuals.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 214_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**9.2.2**Physical and/or logical controls are<br>implemented to restrict use of publicly accessible<br>network jacks within the facility.<br>**Customized Approach Objective**|**9.2.2**Interview responsible personnel and observe<br>locations of publicly accessible network jacks to<br>verify that physical and/or logical controls are in<br>place to restrict access to publicly accessible<br>network jacks within the facility.|Restricting access to network jacks (or network<br>ports) will prevent malicious individuals from<br>plugging into readily available network jacks and<br>gaining access to the CDE or systems connected<br>to the CDE.<br>**Good Practice**|
|Unauthorized devices cannot connect to the entity’s<br>network from public areas within the facility.||Whether logical or physical controls, or a<br>combination of both, are used, they should<br>prevent an individual or device that is not explicitly<br>authorized from being able to connect to the<br>network.<br>**Examples**<br>Methods to meet this requirement include network<br>jacks located in public areas and areas accessible<br>to visitors could be disabled and only enabled<br>when network access is explicitly authorized.<br>Alternatively, processes could be implemented to<br>ensure that visitors are escorted at all times in<br>areas with active network jacks.|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**9.2.3**Physical access to wireless access points,<br>gateways, networking/communications hardware,<br>and telecommunication lines within the facility is<br>restricted.<br>**Customized Approach Objective**<br>Physical networking equipment cannot be accessed<br>by unauthorized personnel.|**9.2.3**Interview responsible personnel and observe<br>locations of hardware and lines to verify that<br>physical access to wireless access points,<br>gateways, networking/communications hardware,<br>and telecommunication lines within the facility is<br>restricted.|Without appropriate physical security over access<br>to wireless components and devices, and<br>computer networking and telecommunications<br>equipment and lines, malicious users could gain<br>access to the entity’s network resources.<br>Additionally, they could connect their own devices<br>to the network to gain unauthorized access to the<br>CDE or systems connected to the CDE.<br>Additionally, securing networking and<br>communications hardware prevents malicious<br>users from intercepting network traffic or<br>physically connecting their own devices to wired<br>network resources.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 215_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**9.2.4**Access to consoles in sensitive areas is<br>restricted via locking when not in use.<br>**Customized Approach Objective**|**9.2.4**Observe a system administrator’s attempt to<br>log into consoles in sensitive areas and verify that<br>they are “locked” to prevent unauthorized use.|Locking console login screens prevents<br>unauthorized persons from gaining access to<br>sensitive information, altering system<br>configurations, introducing vulnerabilities into the<br>network, or destroying records.|
|Physical consoles within sensitive areas cannot be<br>used by unauthorized personnel.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 216_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **9.3 Physical access for personnel and visitors is authorized and managed.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**9.3.1**Procedures are implemented for authorizing<br>and managing physical access of personnel to the<br>CDE, including:|**9.3.1.a**Examine documented procedures to verify<br>that procedures to authorize and manage physical<br>access of personnel to the CDE are defined in<br>|Establishing procedures for granting, managing,<br>and removing access when it is no longer needed<br>ensures non-authorized individuals are prevented<br>from gaining access to areas containing|
|•<br>Identifying personnel.<br>•<br>Managing changes to an individual’s physical|accordance with all elements specified in this<br>requirement.|cardholder data. In addition, it is important to limit<br>access to the actual badging system and badging<br>|
|access requirements.<br>•<br>Revoking or terminating personnel identification.<br>•<br>Limiting access to the identification process or<br>system to authorized personnel.|**9.3.1.b**Observe identification methods, such as ID<br>badges, and processes to verify that personnel in<br>the CDE are clearly identified.|materials to prevent unauthorized personnel from<br>making their own badges and/or setting up their<br>own access rules.<br>**Good Practice**|
||**9.3.1.c**Observe processes to verify that access to<br>the identification process, such as a badge system,|It is important to visually identify the personnel<br>that are physically present, and whether the|
|**Customized Approach Objective**|<br>is limited to authorized personnel.|individual is a visitor or an employee.<br>**Definitions**|
|Requirements for access to the physical CDE are<br>defined and enforced to identify and authorize<br>personnel.||Refer to_Appendix G_for the definition of<br>“personnel.”<br>**Examples**<br>One way to identify personnel is to assign them<br>badges.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 217_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**9.3.1.1**Physical access to sensitive areas within the<br>CDE for personnel is controlled as follows:<br>•<br>Access is authorized and based on individual job<br>function.<br>•<br>Access is revoked immediately upon<br>termination.<br>•<br>All physical access mechanisms, such as keys,|**9.3.1.1.a**Observe personnel in sensitive areas<br>within the CDE, interview responsible personnel,<br>and examine physical access control lists to verify<br>that:<br>•<br>Access to the sensitive area is authorized.<br>•<br>Access is required for the individual’s job<br>function.|Controlling physical access to sensitive areas<br>helps ensure that only authorized personnel with<br>a legitimate business need are granted access.<br>**Good Practice**<br>Where possible, organizations should have<br>policies and procedures to ensure that before<br>personnel leaving the organization, all physical<br>access mechanisms are returned, or disabled as|
|access cards, etc., are returned or disabled<br>upon termination.|**9.3.1.1.b**Observe processes and interview<br>personnel to verify that access of all personnel is<br>revoked immediately upon termination.|soon as possible upon their departure. This will<br>ensure personnel cannot gain physical access to<br>sensitive areas once their employment has<br>ended.|
||**9.3.1.1.c**For terminated personnel, examine<br>physical access controls lists and interview||
|**Customized Approach Objective**<br>Sensitive areas cannot be accessed by<br>unauthorized personnel.|responsible personnel to verify that all physical<br>access mechanisms (such as keys, access cards,<br>etc.) were returned or disabled.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 218_ 



###### **Requirements and Testing Procedures** 

**Defined Approach Requirements Defined Approach Testing Procedures 9.3.2** Procedures are implemented for authorizing **9.3.2.a** Examine documented procedures and and managing visitor access to the CDE, including: interview personnel to verify procedures are • Visitors are authorized before entering. defined for authorizing and managing visitor access to the CDE in accordance with all elements • Visitors are escorted at all times. specified in this requirement. • Visitors are clearly identified and given a badge or other identification that expires. **9.3.2.b** Observe processes when visitors are • Visitor badges or other identification visibly present in the CDE and interview personnel to distinguishes visitors from personnel. verify that visitors are: 

- Authorized before entering the CDE. 

- • Escorted at all times within the CDE. 

###### **Guidance** 

###### **Purpose** 

Visitor controls are important to reduce the ability of unauthorized and malicious persons to gain access to facilities and potentially to cardholder data. 

Visitor controls ensure visitors are identifiable as visitors so personnel can monitor their activities, and that their access is restricted to just the duration of their legitimate visit. 

###### **Definitions** 

Refer to _Appendix G_ for the definition of “visitor.” 

**9.3.2.c** Observe the use of visitor badges or other identification to verify that the badge or other identification does not permit unescorted access to the CDE. 

- **9.3.2.d** Observe visitors in the CDE to verify that: 

- Visitor badges or other identification are being used for all visitors. 

- Visitor badges or identification easily distinguish visitors from personnel. 

**9.3.2.e** Examine visitor badges or other identification and observe evidence in the badging **Customized Approach Objective** system to verify visitor badges or other identification expires. Requirements for visitor access to the CDE are defined and enforced. Visitors cannot exceed any authorized physical access allowed while in the CDE. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 219_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**9.3.3**Visitor badges or identification are<br>surrendered or deactivated before visitors leave the<br>facility or at the date of expiration.<br>**Customized Approach Objective**|**9.3.3**Observe visitors leaving the facility and<br>interview personnel to verify visitor badges or other<br>identification are surrendered or deactivated before<br>visitors leave the facility or at the date of expiration.<br>upon departure or expiration.|Ensuring that visitor badges are returned or<br>deactivated upon expiry or completion of the visit<br>prevents malicious persons from using a<br>previously authorized pass to gain physical<br>access into the building after the visit has ended.|
|Visitor identification or badges cannot be reused<br>after expiration.|||
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**9.3.4**Visitor logs are used to maintain a physical<br>record of visitor activity both within the facility and<br>within sensitive areas, including:<br>•<br>The visitor’s name and the organization<br>|**9.3.4.a**Examine the visitor logs and interview<br>responsible personnel to verify that visitor logs are<br>used to record physical access to both the facility<br>and sensitive areas.|A visitor log documenting minimum information<br>about the visitor is easy and inexpensive to<br>maintain. It will assist in identifying historical<br>physical access to a building or room and<br>potential access to cardholder data.|
|represented.<br>•<br>The date and time of the visit.<br>•<br>The name of the personnel authorizing physical<br>access.<br>•<br>Retaining the log for at least three months,<br>unless otherwise restricted by law.|**9.3.4.b**Examine the visitor logs and verify that the<br>logs contain:<br>•<br>The visitor’s name and the organization<br>represented.<br>•<br>The personnel authorizing physical access.<br>•<br>Date and time of visit.<br>**9.3.4.c**Examine visitor log storage locations and<br>interview responsible personnel to verify that the|**Good Practice**<br>When logging the date and time of visit, including<br>both in and out times is considered a best<br>practice, since it provides helpful tracking<br>information and provides assurance that a visitor<br>has left at the end of the day. It is also good to<br>verify that a visitor’s ID (driver’s license, etc.)<br>matches the name they put on the visitor log.|
|**Customized Approach Objective**|<br>log is retained for at least three months, unless<br>otherwise restricted by law.||
|Records of visitor access that enable the<br>identification of individuals are maintained.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 220_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **9.4 Media with cardholder data is securely stored, accessed, distributed, and destroyed.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**9.4.1**All media with cardholder data is physically<br>secured.|**9.4.1.**Examine documentation to verify that the<br>procedures defined for protecting cardholder data<br>include controls for physically securing all media.|Controls for physically securing media are<br>intended to prevent unauthorized persons from<br>gaining access to cardholder data on any media.<br>Cardholder data is susceptible to unauthorized|
|**Customized Approach Objective**||viewing, copying, or scanning if it is unprotected<br>while it is on removable or portable media, printed|
|Media with cardholder data cannot be accessed by<br>unauthorized personnel.||out, or left on someone’s desk.|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**9.4.1.1**Offline media backups with cardholder data<br>are stored in a secure location.<br>**Customized Approach Objective**<br>Offline backups cannot be accessed by<br>unauthorized personnel.|**9.4.1.1.a**Examine documentation to verify that<br>procedures are defined for physically securing<br>offline media backups with cardholder data in a<br>secure location.<br>**9.4.1.1.b**Examine logs or other documentation<br>and interview responsible personnel at the storage<br>location to verify that offline media backups are<br>stored in a secure location.|If stored in a non-secured facility, backups<br>containing cardholder data may easily be lost,<br>stolen, or copied for malicious intent.<br>**Good Practice**<br>For secure storage of backup media, a good<br>practice is to store media in an off-site facility,<br>such as an alternate or backup site or commercial<br>storage facility.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 221_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**9.4.1.2**The security of the offline media backup<br>location(s) with cardholder data is reviewed at least<br>once every 12 months.|**9.4.1.2.a**Examine documentation to verify that<br>procedures are defined for reviewing the security<br>of the offline media backup location(s) with<br>cardholder data at least once every 12 months.|Conducting regular reviews of the storage facility<br>enables the organization to address identified<br>security issues promptly, minimizing the potential<br>risk. It is important for the entity to be aware of the<br>security of the area where media is being stored.|
|**Customized Approach Objective**|**9.4.1.2.b**Examine documented procedures, logs,<br>or other documentation, and interview responsible<br>personnel at the storage location(s) to verify that<br>the storage location’s security is reviewed at least||
|The security controls protecting offline backups are<br>verified periodically by inspection.|once every 12 months.||
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**9.4.2**All media with cardholder data is classified in<br>accordance with the sensitivity of the data.<br>**Customized Approach Objective**|**9.4.2.a**Examine documentation to verify that<br>procedures are defined for classifying media with<br>cardholder data in accordance with the sensitivity<br>of the data.<br>**9.4.2.b**Examine media logs or other<br>documentation to verify that all media is classified<br>in accordance with the sensitivity of the data.|Media not identified as confidential may not be<br>adequately protected or may be lost or stolen.<br>**Good Practice**<br>It is important that media be identified such that<br>its classification status is apparent. This does not<br>mean however that the media needs to have a<br>“confidential” label.|
|Media are classified and protected appropriately.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 222_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**9.4.3**Media with cardholder data sent outside the<br>facility is secured as follows:<br>•<br>Media sent outside the facility is logged.<br>•<br>Media is sent by secured courier or other|**9.4.3.a**Examine documentation to verify that<br>procedures are defined for securing media sent<br>outside the facility in accordance with all elements<br>specified in this requirement.|Media may be lost or stolen if sent via a non-<br>trackable method such as regular postal mail. The<br>use of secure couriers to deliver any media that<br>contains cardholder data allows organizations to<br>use their tracking systems to maintain inventory<br>|
|delivery method that can be accurately tracked.<br>•<br>Offsite tracking logs include details about media<br>location.|**9.4.3.b**Interview personnel and examine records<br>to verify that all media sent outside the facility is<br>logged and sent via secured courier or other<br>delivery method that can be tracked.|and location of shipments.|
|**Customized Approach Objective**|**9.4.3.c**Examine offsite tracking logs for all media<br>to verify tracking details are documented.||
|Media is secured and tracked when transported<br>outside the facility.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 223_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**9.4.4**Management approves all media with<br>cardholder data that is moved outside the facility<br>(including when media is distributed to individuals).|**9.4.4.a**Examine documentation to verify that<br>procedures are defined to ensure that media<br>moved outside the facility is approved by<br>management.|Without a firm process for ensuring that all media<br>movements are approved before the media is<br>removed from secure areas, the media would not<br>be tracked or appropriately protected, and its<br>location would be unknown, leading to lost or<br>|
|**Customized Approach Objective**<br>Media cannot leave a facility without the approval of<br>accountable personnel.|**9.4.4.b**Examine offsite media tracking logs and<br>interview responsible personnel to verify that<br>proper management authorization is obtained for<br>all media moved outside the facility (including<br>media distributed to individuals).|stolen media.|
|**Applicability Notes**|||
|Individuals approving media movements should<br>have the appropriate level of management authority<br>to grant this approval. However, it is not specifically<br>required that such individuals have “manager” as<br>part of their title.|||
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**9.4.5**Inventory logs of all electronic media with<br>cardholder data are maintained.|**9.4.5.a**Examine documentation to verify that<br>procedures are defined to maintain electronic<br>media inventory logs.|Without careful inventory methods and storage<br>controls, stolen or missing electronic media could<br>go unnoticed for an indefinite amount of time.|
|**Customized Approach Objective**|**9.4.5.b**Examine electronic media inventory logs<br>and interview responsible personnel to verify that<br>logs are maintained.||
|Accurate inventories of stored electronic media are<br>maintained.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 224_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**9.4.5.1**Inventories of electronic media with<br>cardholder data are conducted at least once every<br>12 months.|**9.4.5.1.a**Examine documentation to verify that<br>procedures are defined to conduct inventories of<br>electronic media with cardholder data at least once<br>every 12 months.|Without careful inventory methods and storage<br>controls, stolen or missing electronic media could<br>go unnoticed for an indefinite amount of time.|
|**Customized Approach Objective**<br>Media inventories are verified periodically.|**9.4.5.1.b**Examine electronic media inventory logs<br>and interview personnel to verify that electronic<br>media inventories are performed at least once<br>every 12 months.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 225_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**9.4.6**Hard-copy materials with cardholder data are<br>destroyed when no longer needed for business or<br>legal reasons, as follows:<br>•<br>Materials are cross-cut shredded, incinerated, or<br>pulped so that cardholder data cannot be<br>reconstructed.|**9.4.6.a**Examine the media destruction policy to<br>verify that procedures are defined to destroy hard-<br>copy media with cardholder data when no longer<br>needed for business or legal reasons in<br>accordance with all elements specified in this<br>requirement.|If steps are not taken to destroy information<br>contained on hard-copy media before disposal,<br>malicious individuals may retrieve information<br>from the disposed media, leading to a data<br>compromise. For example, malicious individuals<br>may use a technique known as “dumpster diving,”<br>where they search through trashcans and recycle|
|•<br>Materials are stored in secure storage<br>containers prior to destruction.|**9.4.6.b**Observe processes and interview<br>personnel to verify that hard-copy materials are<br>cross-cut shredded, incinerated, or pulped such<br>that cardholder data cannot be reconstructed.|bins looking for hard-copy materials with<br>information they can use to launch an attack.<br>Securing storage containers used for materials<br>that are going to be destroyed prevents sensitive<br>information from being captured while the|
||**9.4.6.c**Observe storage containers used for<br>materials that contain information to be destroyed|materials are being collected.<br>**Good Practice**|
|**Customized Approach Objective**|to verify that the containers are secure.|Consider “to-be-shredded” containers with a lock<br>that prevents access to its contents or that|
|Cardholder data cannot be recovered from media<br>that has been destroyed or which is pending<br>destruction.||physically prevent access to the inside of the<br>container.<br>**Further Information**<br>See_NIST Special Publication 800-88, Revision 1:_|
|**Applicability Notes**||_Guidelines for Media Sanitization_.|
|These requirements for media destruction when that<br>media is no longer needed for business or legal<br>reasons are separate and distinct from PCI DSS<br>Requirement 3.2.1, which is for securely deleting<br>cardholder data when no longer needed per the<br>entity’s cardholder data retention policies.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 226_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**9.4.7**Electronic media with cardholder data is<br>destroyed when no longer needed for business or<br>legal reasons via one of the following:<br>•<br>The electronic media is destroyed.<br>•<br>The cardholder data is rendered unrecoverable<br>so that it cannot be reconstructed.<br>**Customized Approach Objective**|**9.4.7.a**Examine the media destruction policy to<br>verify that procedures are defined to destroy<br>electronic media when no longer needed for<br>business or legal reasons in accordance with all<br>elements specified in this requirement.<br>**9.4.7.b**Observe the media destruction process<br>and interview responsible personnel to verify that<br>electronic media with cardholder data is destroyed<br>via one of the methods specified in this|If steps are not taken to destroy information<br>contained on electronic media when no longer<br>needed, malicious individuals may retrieve<br>information from the disposed media, leading to a<br>data compromise. For example, malicious<br>individuals may use a technique known as<br>“dumpster diving,” where they search through<br>trashcans and recycle bins looking for information<br>they can use to launch an attack.<br>**Good Practice**|
|Cardholder data cannot be recovered from media<br>that has been erased or destroyed.|requirement.|The deletion function in most operating systems<br>allows deleted data to be recovered, so instead, a<br>dedicated secure deletion function or application|
|**Applicability Notes**||should be used to make data unrecoverable.<br>**Examples**|
|These requirements for media destruction when that<br>media is no longer needed for business or legal<br>reasons are separate and distinct from PCI DSS<br>Requirement 3.2.1, which is for securely deleting<br>cardholder data when no longer needed per the<br>entity’s cardholder data retention policies.||Methods for securely destroying electronic media<br>include secure wiping in accordance with<br>industry-accepted standards for secure deletion,<br>degaussing, or physical destruction (such as<br>grinding or shredding hard disks).<br>**Further Information**<br>See_NIST Special Publication 800-88, Revision 1:_<br>_Guidelines for Media Sanitization_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 227_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **9.5 Point-of-interaction (POI) devices are protected from tampering and unauthorized substitution.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**9.5.1**POI devices that capture payment card data<br>via direct physical interaction with the payment card<br>form factor are protected from tampering and<br>unauthorized substitution, including the following:<br>•<br>Maintaining a list of POI devices.|**9.5.1**Examine documented policies and<br>procedures to verify that processes are defined<br>that include all elements specified in this<br>requirement.|Criminals attempt to steal payment card data by<br>stealing and/or manipulating card-reading devices<br>and terminals. Criminals will try to steal devices<br>so they can learn how to break into them, and<br>they often try to replace legitimate devices with<br>fraudulent devices that send them payment card|
|•<br>Periodically inspecting POI devices to look for||data every time a card is entered.|
|tampering or unauthorized substitution.||They will also try to add “skimming” components|
|•<br>Training personnel to be aware of suspicious<br>behavior and to report tampering or<br>unauthorized substitution of devices.||to the outside of devices, which are designed to<br>capture payment card data before it enters the<br>device—for example, by attaching an additional<br>card reader on top of the legitimate card reader|
|**Customized Approach Objective**||so that the payment card data is captured twice:<br>once by the criminal’s component and then by the|
|The entity has defined procedures to protect and<br>manage point-of-interaction devices. Expectations,<br>controls, and oversight for the management and<br>protection of POI devices are defined and adhered<br>to by affected personnel.||device’s legitimate component. In this way,<br>transactions may still be completed without<br>interruption while the criminal is “skimming” the<br>payment card data during the process.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 228_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Applicability Notes**<br>These requirements apply to deployed POI devices<br>used in card-present transactions (that is, a<br>payment card form factor such as a card that is<br>swiped, tapped, or dipped).<br>These requirements do not apply to:<br>•<br>Components used only for manual PAN key<br>entry.<br>•<br>Commercial off-the-shelf (COTS) devices (for<br>example, smartphones or tablets), which are<br>mobile merchant-owned devices designed for<br>mass-market distribution.||_(continued on next page)_<br>**Good Practice**<br>Entities may consider implementing protection<br>from tampering and unauthorized substitution for:<br>•<br>Components used only for manual PAN key<br>entry.<br>•<br>Commercial off-the-shelf (COTS) devices (for<br>example, smartphones or tablets), which are<br>mobile merchant-owned devices designed for<br>mass-market distribution.<br>**Further Information**<br>Additional best practices on skimming prevention<br>are available on the PCI SSC website.|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**9.5.1.1**An up-to-date list of POI devices is<br>maintained, including:<br>|**9.5.1.1.a**Examine the list of POI devices to verify it<br>includes all elements specified in this requirement.|Keeping an up-to-date list of POI devices helps<br>an organization track where devices are<br>supposed to be and quickly identify if a device is|
|•<br>Make and model of the device.<br>•<br>Location of device.<br>•<br>Device serial number or other methods of<br>unique identification.|**9.5.1.1.b**Observe POI devices and device<br>locations and compare to devices in the list to<br>verify that the list is accurate and up to date.|missing or lost.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 229_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Customized Approach Objective**<br>The identity and location of POI devices is recorded<br>and known at all times.|**9.5.1.1.c**Interview personnel to verify the list of<br>POI devices is updated when devices are added,<br>relocated, decommissioned, etc.|**Good Practice**<br>The method for maintaining a list of devices may<br>be automated (for example, a device-<br>management system) or manual (for example,<br>documented in electronic or paper records). For<br>on-the-road devices, the location may include the<br>name of the personnel to whom the device is<br>assigned.<br>**Examples**<br>Methods to maintain device locations include<br>identifying the address of the site or facility where<br>the device is located.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 230_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**9.5.1.2**POI device surfaces are periodically<br>inspected to detect tampering and unauthorized<br>substitution.|**9.5.1.2.a**Examine documented procedures to<br>verify processes are defined for periodic<br>inspections of POI device surfaces to detect<br>tampering and unauthorized substitution.|Regular inspections of devices will help<br>organizations detect tampering more quickly via<br>external evidence—for example, the addition of a<br>card skimmer—or replacement of a device,<br>thereby minimizing the potential impact of using|
|**Customized Approach Objective**|**9.5.1.2.b**Interview responsible personnel and<br>observe inspection processes to verify:<br>•<br>Personnel are aware of procedures for<br>inspecting devices.<br>•<br>All devices are periodically inspected for<br>|fraudulent devices.<br>**Good Practice**<br>Methods for periodic inspection include checking<br>the serial number or other device characteristics<br>and comparing the information to the list of POI<br>devices to verify the device has not been|
|Point of interaction devices cannot be tampered<br>with, substituted without authorization, or have|evidence of tampering and unauthorized<br>substitution.|swapped with a fraudulent device.|
|skimming attachments installed without timely<br>detection.||_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 231_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**9.5.1.2** _(continued)_|**Examples**<br>The type of inspection will depend on the device.<br>For instance, photographs of devices known to be<br>secure can be used to compare a device’s current<br>appearance with its original appearance to see<br>whether it has changed. Another option may be to<br>use a secure marker pen, such as a UV light<br>marker, to mark device surfaces and device<br>openings so any tampering or replacement will be<br>apparent. Criminals will often replace the outer<br>casing of a device to hide their tampering, and<br>these methods may help to detect such activities.<br>Device vendors may also provide security<br>guidance and “how to” guides to help determine<br>whether the device has been subject to<br>tampering.<br>Signs that a device might have been tampered<br>with or substituted include:<br>•<br>Unexpected attachments or cables plugged<br>into the device.<br>•<br>Missing or changed security labels.<br>•<br>Broken or differently colored casing.<br>•<br>Changes to the serial number or other<br>external markings.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 232_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**9.5.1.2.1**The frequency of periodic POI device<br>inspections and the type of inspections performed is<br>defined in the entity’s targeted risk analysis, which is<br>performed according to all elements specified in|**9.5.1.2.1.a**Examine the entity’s targeted risk<br>analysis for the frequency of periodic POI device<br>inspections and type of inspections performed to<br>verify the risk analysis was performed in|Entities are best placed to determine the<br>frequency of POI device inspections based on the<br>environment in which the device operates.<br>**Good Practice**|
|Requirement 12.3.1.|accordance with all elements specified in<br>Requirement 12.3.1.|The frequency of inspections will depend on<br>factors such as the location of a device and<br>whether the device is attended or unattended. For|
||**9.5.1.2.1.b**Examine documented results of<br>periodic device inspections and interview|example, devices left in public areas without<br>supervision by the organization’s personnel might|
|**Customized Approach Objective**|<br>personnel to verify that the frequency and type of<br>POI device inspections performed match what is|have more frequent inspections than devices kept<br>in secure areas or supervised when accessible to|
|POI devices are inspected at a frequency that<br>addresses the entity’s risk.|<br>defined in the entity’s targeted risk analysis<br>conducted for this requirement.|the public. In addition, many POI vendors include<br>guidance in their user documentation about how<br>often POI devices should be checked, and for|
|**Applicability Notes**||what – entities should consult their vendors’<br>documentation and incorporate those|
|_This requirement is a best practice until 31 March_||recommendations into their periodic inspections.|
|_2025, after which it will be required and must be_|||
|_fully considered during a PCI DSS assessment._|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 233_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**9.5.1.3**Training is provided for personnel in POI<br>environments to be aware of attempted tampering<br>or replacement of POI devices, and includes:<br>|**9.5.1.3.a**Review training materials for personnel in<br>POI environments to verify they include all<br>elements specified in this requirement.|Criminals will often pose as authorized<br>maintenance personnel to gain access to POI<br>devices.<br>**Good Practice**|
|•<br>Verifying the identity of any third-party persons<br>claiming to be repair or maintenance personnel,<br>before granting them access to modify or<br>troubleshoot devices.<br>•<br>Procedures to ensure devices are not installed,<br>replaced, or returned without verification.|**9.5.1.3.b**Interview personnel in POI environments<br>to verify they have received training and know the<br>procedures for all elements specified in this<br>requirement**.**|Personnel training should include being alert to<br>and questioning anyone who shows up to do POI<br>maintenance to ensure they are authorized and<br>have a valid work order, including any agents,<br>maintenance or repair personnel, technicians,<br>service providers, or other third parties. All third|
|•<br>Being aware of suspicious behavior around<br>devices.||parties requesting access to devices should<br>always be verified before being provided|
|•<br>Reporting suspicious behavior and indications of<br>device tampering or substitution to appropriate<br>personnel.||access—for example, by checking with<br>management or phoning the POI maintenance<br>company, such as the vendor or acquirer, for<br>verification. Many criminals will try to fool|
|**Customized Approach Objective**||personnel by dressing for the part (for example,<br>carrying toolboxes and dressed in work apparel),|
|Personnel are knowledgeable about the types of<br>attacks against POI devices, the entity’s technical<br>and procedural countermeasures, and can access<br>assistance and guidance when required.||and could also be knowledgeable about locations<br>of devices, so personnel should be trained to<br>always follow procedures.<br>Another trick that criminals use is to send a “new”<br>POI device with instructions for swapping it with a<br>legitimate device and “returning” the legitimate<br>device. The criminals may even provide return<br>postage to their specified address. Therefore,<br>personnel should always verify with their manager<br>or supplier that the device is legitimate and came<br>from a trusted source before installing it or using it<br>for business.|
|||_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 234_ 



||**Requirements and Testing Procedures**|**Guidance**|
|---|---|---|
|**9.5.1.3**_(continued)_||**Examples**<br>Suspicious behavior that personnel should be<br>aware of includes attempts by unknown persons<br>to unplug or open devices.<br>Ensuring personnel are aware of mechanisms for<br>reporting suspicious behavior and who to report<br>such behavior to—for example, a manager or<br>security officer—will help reduce the likelihood<br>and potential impact of a device being tampered<br>with or substituted.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 235_ 



### **Regularly Monitor and Test Networks** 

#### **_Requirement 10: Log and Monitor All Access to System Components and Cardholder Data_** 

**Sections** 

- **10.1** Processes and mechanisms for logging and monitoring all access to system components and cardholder data are defined and understood. 

- **10.2** Audit logs are implemented to support the detection of anomalies and suspicious activity, and the forensic analysis of events. 

- **10.3** Audit logs are protected from destruction and unauthorized modifications. 

- **10.4** Audit logs are reviewed to identify anomalies or suspicious activity. 

- **10.5** Audit log history is retained and available for analysis. 

- **10.6** Time-synchronization mechanisms support consistent time settings across all systems. 

- **10.7** Failures of critical security control systems are detected, reported, and responded to promptly. 

###### **Overview** 

Logging mechanisms and the ability to track user activities are critical in preventing, detecting, or minimizing the impact of a data compromise. The presence of logs on all system components and in the cardholder data environment (CDE) allows thorough tracking, alerting, and analysis when something does go wrong. Determining the cause of a compromise is difficult, if not impossible, without system activity logs. 

This requirement applies to user activities, including those by employees, contractors, consultants, and internal and external vendors, and other third parties (for example, those providing support or maintenance services). 

These requirements do not apply to user activity of consumers (cardholders). 

Refer to _Appendix G_ for definitions of PCI DSS terms. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 236_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

**10.1 Processes and mechanisms for logging and monitoring all access to system components and cardholder data are defined and understood.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**10.1.1**All security policies and operational<br>procedures that are identified in Requirement 10<br>are:<br>•<br>Documented.<br>•<br>Kept up to date.<br>•<br>In use.<br>•<br>Known to all affected parties.|**10.1.1**Examine documentation and interview<br>personnel to verify that security policies and<br>operational procedures identified in Requirement<br>10 are managed in accordance with all elements<br>specified in this requirement.|Requirement 10.1.1 is about effectively managing<br>and maintaining the various policies and<br>procedures specified throughout Requirement 10.<br>While it is important to define the specific policies<br>or procedures called out in Requirement 10, it is<br>equally important to ensure they are properly<br>documented, maintained, and disseminated.<br>**Good Practice**<br>It is important to update policies and procedures<br>as needed to address changes in processes,<br>technologies, and business objectives. For this|
|**Customized Approach Objective**||reason, consider updating these documents as<br>soon as possible after a change occurs and not|
|Expectations, controls, and oversight for meeting<br>activities within Requirement 10 are defined and||only on a periodic cycle.<br>**Definitions**|
|adhered to by affected personnel. All supporting<br>activities are repeatable, consistently applied, and<br>conform to management’s intent.||Security policies define the entity’s security<br>objectives and principles. Operational procedures<br>describe how to perform activities, and define the<br>controls, methods, and processes that are<br>followed to achieve the desired result in a<br>consistent manner and in accordance with policy<br>objectives.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 237_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**10.1.2**Roles and responsibilities for performing<br>activities in Requirement 10 are documented,<br>assigned, and understood.|**10.1.2.a**Examine documentation to verify that<br>descriptions of roles and responsibilities for<br>performing activities in Requirement 10 are<br>documented and assigned.|If roles and responsibilities are not formally<br>assigned, personnel may not be aware of their<br>day-to-day responsibilities and critical activities<br>may not occur.<br>**Good Practice**|
||**10.1.2.b**Interview personnel with responsibility for<br>performing activities in Requirement 10 to verify|Roles and responsibilities may be documented<br>within policies and procedures or maintained|
|**Customized Approach Objective**<br>Day-to-day responsibilities for performing all the<br>activities in Requirement 10 are allocated.<br>Personnel are accountable for successful,<br>continuous operation of these requirements.|<br>that roles and responsibilities are assigned as<br>defined and are understood.|within separate documents.<br>As part of communicating roles and<br>responsibilities, entities can consider having<br>personnel acknowledge their acceptance and<br>understanding of their assigned roles and<br>responsibilities.<br>**Examples**<br>A method to document roles and responsibilities<br>is a responsibility assignment matrix that includes<br>who is responsible, accountable, consulted, and<br>informed (also called a RACI matrix).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 238_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

**10.2 Audit logs are implemented to support the detection of anomalies and suspicious activity, and the forensic analysis of events.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**10.2.1**Audit logs are enabled and active for all<br>system components and cardholder data.<br>**Customized Approach Objective**|**10.2.1**Interview the system administrator and<br>examine system configurations to verify that audit<br>logs are enabled and active for all system<br>components.|Audit logs must exist for all system components.<br>Audit logs send alerts the system administrator,<br>provides data to other monitoring mechanisms,<br>such as intrusion-detection systems (IDS) and<br>security information and event monitoring<br>systems (SIEM) tools, and provide a history trail<br>for post-incident investigation.|
|Records of all activities affecting system<br>components and cardholder data are captured.||Logging and analyzing security-relevant events<br>enable an organization to identify and trace<br>potentially malicious activities.<br>**Good Practice**<br>When an entity considers which information to<br>record in their logs, it is important to remember<br>that information stored in audit logs is sensitive<br>and should be protected per requirements in this<br>standard. Care should be taken to only store<br>essential information in the audit logs to minimize<br>risk.|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**10.2.1.1**Audit logs capture all individual user<br>access to cardholder data.<br>**Customized Approach Objective**<br>Records of all individual user access to cardholder<br>data are captured.|**10.2.1.1**Examine audit log configurations and log<br>data to verify that all individual user access to<br>cardholder data is logged.|It is critical to have a process or system that links<br>user access to system components accessed.<br>Malicious individuals could obtain knowledge of a<br>user account with access to systems in the CDE,<br>or they could create a new, unauthorized account<br>to access cardholder data.<br>**Good Practice**<br>A record of all individual access to cardholder<br>data can identify which accounts may have been<br>compromised or misused.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 239_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**10.2.1.2**Audit logs capture all actions taken by any<br>individual with administrative access, including any<br>interactive use of application or system accounts.<br>**Customized Approach Objective**|**10.2.1.2**Examine audit log configurations and log<br>data to verify that all actions taken by any<br>individual with administrative access, including any<br>interactive use of application or system accounts,<br>are logged.|Accounts with increased access privileges, such<br>as the “administrator” or “root” account, have the<br>potential to significantly impact the security or<br>operational functionality of a system. Without a<br>log of the activities performed, an organization is<br>cannot trace any issues resulting from an<br>administrative mistake or misuse of privilege back|
|Records of all actions performed by individuals with<br>elevated privileges are captured.||<br>to the specific action and account.<br>**Definitions**<br>The functions or activities considered to be<br>administrative are beyond those performed by<br>regular users as part of routine business<br>functions.<br>Refer to_Appendix G_for the definition of<br>“administrative access.”|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**10.2.1.3**Audit logs capture all access to audit logs.<br>**Customized Approach Objective**|**10.2.1.3**Examine audit log configurations and log<br>data to verify that access to all audit logs is<br>captured.|Malicious users often attempt to alter audit logs to<br>hide their actions. A record of access allows an<br>organization to trace any inconsistencies or<br>potential tampering of the logs to an individual<br>account. Having logs identify changes, additions,<br>and deletions to the audit logs can help retrace|
|Records of all access to audit logs are captured.||steps made by unauthorized personnel.|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**10.2.1.4**Audit logs capture all invalid logical access<br>attempts.||Malicious individuals will often perform multiple<br>access attempts on targeted systems. Multiple|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 240_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Customized Approach Objective**<br>Records of all invalid access attempts are captured.|**10.2.1.4**Examine audit log configurations and log<br>data to verify that invalid logical access attempts<br>are captured.|invalid login attempts may be an indication of an<br>unauthorized user’s attempts to “brute force” or<br>guess a password.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 241_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**10.2.1.5**Audit logs capture all changes to<br>identification and authentication credentials<br>including, but not limited to:<br>•<br>Creation of new accounts.<br>•<br>Elevation of privileges.<br>•<br>All changes, additions, or deletions to accounts<br>with administrative access.<br>**Customized Approach Objective**|**10.2.1.5**Examine audit log configurations and log<br>data to verify that changes to identification and<br>authentication credentials are captured in<br>accordance with all elements specified in this<br>requirement.|Logging changes to authentication credentials<br>(including elevation of privileges, additions, and<br>deletions of accounts with administrative access)<br>provides residual evidence of activities.<br>Malicious users may attempt to manipulate<br>authentication credentials to bypass them or<br>impersonate a valid account.|
|Records of all changes to identification and<br>authentication credentials are captured.<br>**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**10.2.1.6**Audit logs capture the following:<br>•<br>All initialization of new audit logs, and<br>•<br>All starting, stopping, or pausing of the existing<br>audit logs.|**10.2.1.6**Examine audit log configurations and log<br>data to verify that all elements specified in this<br>requirement are captured.|Turning off or pausing audit logs before<br>performing illicit activities is common practice for<br>malicious users who want to avoid detection.<br>Initialization of audit logs could indicate that that a<br>user disabled the log function to hide their<br>actions.|



**Customized Approach Objective** Records of all changes to audit log activity status are captured. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 242_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**10.2.1.7**Audit logs capture all creation and deletion<br>of system-level objects.<br>**Customized Approach Objective**<br>Records of alterations that indicate a system has<br>been modified from its intended functionality are<br>captured.|**10.2.1.7**Examine audit log configurations and log<br>data to verify that creation and deletion of system<br>level objects is captured.|Malicious software, such as malware, often<br>creates or replaces system-level objects on the<br>target system to control a particular function or<br>operation on that system. By logging when<br>system-level objects are created or deleted, it will<br>be easier to determine whether such<br>modifications were authorized.|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**10.2.2**Audit logs record the following details for<br>each auditable event:<br>•<br>User identification.<br>•<br>Type of event.<br>•<br>Date and time.<br>•<br>Success and failure indication.<br>•<br>Origination of event.<br>•<br>Identity or name of affected data, system<br>component, resource, or service (for example,<br>name and protocol).|**10.2.2**Interview personnel and examine audit log<br>configurations and log data to verify that all<br>elements specified in this requirement are included<br>in log entries for each auditable event (from<br>10.2.1.1 through 10.2.1.7).|By recording these details for the auditable events<br>at 10.2.1.1 through 10.2.1.7, a potential<br>compromise can be quickly identified, with<br>sufficient detail to facilitate following up on<br>suspicious activities.|
|**Customized Approach Objective**|||
|Sufficient data to be able to identify successful and<br>failed attempts and who, what, when, where, and<br>how for each event listed in requirement 10.2.1 are<br>captured.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 243_ 



###### **Requirements and Testing Procedures Guidance** 

###### **10.3 Audit logs are protected from destruction and unauthorized modifications.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**10.3.1**Read access to audit logs files is limited to<br>those with a job-related need.<br>**Customized Approach Objective**|**10.3.1**Interview system administrators and<br>examine system configurations and privileges to<br>verify that only individuals with a job-related need<br>have read access to audit log files.|Audit log files contain sensitive information, and<br>read access to the log files must be limited only to<br>those with a valid business need. This access<br>includes audit log files on the originating systems<br>as well as anywhere else they are stored.<br>**Good Practice**|
|Stored activity records cannot be accessed by<br>unauthorized personnel.||Adequate protection of the audit logs includes<br>strong access control that limits access to logs<br>based on “need to know” only and the use of<br>physical or network segregation to make the logs<br>harder to find and modify.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 244_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**10.3.2**Audit log files are protected to prevent<br>modifications by individuals.<br>**Customized Approach Objective**|**10.3.2**Examine system configurations and<br>privileges and interview system administrators to<br>verify that current audit log files are protected from<br>modifications by individuals via access control<br>mechanisms, physical segregation, and/or network<br>segregation.|Often a malicious individual who has entered the<br>network will try to edit the audit logs to hide their<br>activity. Without adequate protection of audit logs,<br>their completeness, accuracy, and integrity<br>cannot be guaranteed, and the audit logs can be<br>rendered useless as an investigation tool after a<br>compromise. Therefore, audit logs should be|
|Stored activity records cannot be modified by<br>personnel.||protected on the originating systems as well as<br>anywhere else they are stored.<br>**Good Practice**<br>Entities should attempt to prevent logs from being<br>exposed in public-accessible locations.|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**10.3.3**Audit log files, including those for external-<br>facing technologies, are promptly backed up to a<br>secure, central, internal log server(s) or other media<br>that is difficult to modify.<br>**Customized Approach Objective**<br>Stored activity records are secured and preserved in<br>a central location to prevent unauthorized<br>modification.|**10.3.3**Examine backup configurations or log files<br>to verify that current audit log files, including those<br>for external-facing technologies, are promptly<br>backed up to a secure, central, internal log<br>server(s) or other media that is difficult to modify.|Promptly backing up the logs to a centralized log<br>server or media that is difficult to alter keeps the<br>logs protected, even if the system generating the<br>logs becomes compromised.<br>Writing logs from external-facing technologies<br>such as wireless, network security controls, DNS,<br>and mail servers, reduces the risk of those logs<br>being lost or altered.<br>**Good Practice**<br>Each entity determines the best way to back up<br>log files, whether via one or more centralized log<br>servers or other secure media. Logs may be<br>written directly, offloaded, or copied from external<br>systems to the secure internal system or media.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 245_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**10.3.4**File integrity monitoring or change-detection<br>mechanisms is used on audit logs to ensure that<br>existing log data cannot be changed without<br>generating alerts.<br>**Customized Approach Objective**|**10.3.4**Examine system settings, monitored files,<br>and results from monitoring activities to verify the<br>use of file integrity monitoring or change-detection<br>software on audit logs.|File integrity monitoring or change-detection<br>systems check for changes to critical files and<br>notify when such changes are identified. For file<br>integrity monitoring purposes, an entity usually<br>monitors files that do not regularly change, but<br>when changed, indicate a possible compromise.<br>**Good Practice**|
|Stored activity records cannot be modified without<br>an alert being generated.||Software used to monitor changes to audit logs<br>should be configured to provide alerts when<br>existing log data or files are changed or deleted.<br>However, new log data being added to an audit<br>log should not generate an alert.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 246_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**10.4** **Audit logs are reviewed to identify anomali**|**es or suspicious activity.**||
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**<br>|
|**10.4.1**The following audit logs are reviewed at least<br>once daily:<br>•<br>All security events.<br>•<br>Logs of all system components that store, process,|**10.4.1.a**Examine security policies and procedures to<br>verify that processes are defined for reviewing all<br>elements specified in this requirement at least once<br>daily.|Many breaches occur months before being detected.<br>Regular log reviews mean incidents can be quickly<br>identified and proactively addressed.<br>**Good Practice**<br>Checking logs daily (7 days a week, 365 days a|
|or transmit CHD and/or SAD.<br>•<br>Logs of all critical system components.<br>•<br>Logs of all servers and system components that<br>perform security functions (for example, network<br>security controls, intrusion-detection<br>systems/intrusion-prevention systems (IDS/IPS),<br>authentication servers).<br>**Customized Approach Objective**<br>Potentially suspicious or anomalous activities are<br>quickly identified to minimize impact.|**10.4.1.b**Observe processes and interview<br>personnel to verify that all elements specified in<br>this requirement are reviewed at least once daily|year, including holidays) minimizes the amount of<br>time and exposure of a potential breach. Log<br>harvesting, parsing, and alerting tools, centralized<br>log management systems, event log analyzers, and<br>security information and event management (SIEM)<br>solutions are examples of automated tools that can<br>be used to meet this requirement.<br>Daily review of security events—for example,<br>notifications or alerts that identify suspicious or<br>anomalous activities—as well as logs from critical<br>system components, and logs from systems that<br>perform security functions, such as firewalls,<br>IDS/IPS, file integrity monitoring (FIM) systems, etc.,<br>is necessary to identify potential issues.<br>The determination of “security event” will vary for<br>each organization and may include consideration for<br>the type of technology, location, and function of the<br>device. Organizations may also wish to maintain a<br>baseline of “normal” traffic to help identify anomalous<br>behavior.|



An entity that uses third-party service providers to perform log review services is responsible to provide context about the entity’s environment to the service providers, so it understands the entity’s environment, has a baseline of “normal” traffic for the entity, and can detect potential security issues and provide accurate exceptions and anomaly notifications. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 247_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**10.4.1.1**Automated mechanisms are used to<br>perform audit log reviews.<br>**Customized Approach Objective**|**10.4.1.1**Examine log review mechanisms and<br>interview personnel to verify that automated<br>mechanisms are used to perform log reviews.|Manual log reviews are difficult to perform, even<br>for one or two systems, due to the amount of log<br>data that is generated. However, using log<br>harvesting, parsing, and alerting tools, centralized<br>log management systems, event log analyzers,|
|Potentially suspicious or anomalous activities are<br>identified via a repeatable and consistent<br>mechanism.||and security information and event management<br>(SIEM) solutions can help facilitate the process by<br>identifying log events that need to be reviewed.<br>**Good Practice**|
|**Applicability Notes**||Establishing a baseline of normal audit activity<br>patterns is critical to the effectiveness of an|
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._||automated log review mechanism. The analysis of<br>new audit activity against the established baseline<br>can significantly improve the identification of<br>suspicious or anomalous activities.<br>The entity should keep logging tools aligned with<br>any changes in their environment by periodically<br>reviewing tool settings and updating settings to<br>reflect any changes.<br>**Further Information**<br>Refer to the Information Supplement:_Effective_<br>_Daily Log Monitoring_for additional guidance.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 248_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**10.4.2**Logs of all other system components (those<br>not specified in Requirement 10.4.1) are reviewed<br>periodically.|**10.4.2.a**Examine security policies and procedures<br>to verify that processes are defined for reviewing<br>logs of all other system components periodically.|Periodic review of logs for all other system<br>components (not specified in Requirement 10.4.1)<br>helps to identify indications of potential issues or<br>attempts to access critical systems via less-critical<br>|
|**Customized Approach Objective**|**10.4.2.b**Examine documented results of log<br>reviews and interview personnel to verify that log<br>reviews are performed periodically.|systems.|
|Potentially suspicious or anomalous activities for<br>other system components (not included in 10.4.1)<br>are reviewed in accordance with the entity’s<br>identified risk.|||
|**Applicability Notes**|||
|This requirement is applicable to all other in-scope<br>system components not included in Requirement<br>10.4.1.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 249_ 



###### **Requirements and Testing Procedures** 

**Defined Approach Requirements Defined Approach Testing Procedures 10.4.2.1** The frequency of periodic log reviews for **10.4.2.1.a** Examine the entity’s targeted risk all other system components (not defined in analysis for the frequency of periodic log reviews Requirement 10.4.1) is defined in the entity’s for all other system components (not defined in targeted risk analysis, which is performed Requirement 10.4.1) to verify the risk analysis was according to all elements specified in Requirement performed in accordance with all elements 12.3.1 specified at Requirement 12.3.1. **10.4.2.1.b** Examine documented results of periodic log reviews of all other system components (not **Customized Approach Objective** defined in Requirement 10.4.1) and interview personnel to verify log reviews are performed at Log reviews for lower-risk system components are the frequency specified in the entity’s targeted risk performed at a frequency that addresses the entity’s analysis performed for this requirement. risk. **Applicability Notes** _This requirement is a best practice until 31 March 2025, after which it will be required and must be fully considered during a PCI DSS assessment._ 

###### **Guidance** 

###### **Purpose** 

Entities can determine the optimum period to review these logs based on criteria such as the complexity of each entity’s environment, the number of types of systems that are required to be evaluated, and the functions of such systems. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 250_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**10.4.3**Exceptions and anomalies identified during<br>the review process are addressed.|**10.4.3.a**Examine security policies and procedures<br>to verify that processes are defined for addressing<br>exceptions and anomalies identified during the<br>review process.|If exceptions and anomalies identified during the<br>log-review process are not investigated, the entity<br>may be unaware of unauthorized and potentially<br>malicious activities occurring within their network.<br>**Good Practice**|
|**Customized Approach Objective**|**10.4.3.b**Observe processes and interview<br>personnel to verify that, when exceptions and<br>anomalies are identified, they are addressed.|Entities should consider how to address the<br>following when developing their processes for<br>defining and managing exceptions and<br>anomalies:|
|Suspicious or anomalous activities are addressed.||•<br>How log review activities are recorded,<br>•<br>How to rank and prioritize exceptions and<br>anomalies,<br>•<br>What procedures should be in place to report<br>and escalate exceptions and anomalies, and<br>•<br>Who is responsible for investigating and for<br>any remediation tasks.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 251_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **10.5 Audit log history is retained and available for analysis.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**10.5.1**Retain audit log history for at least 12<br>months, with at least the most recent three months<br>immediately available for analysis.|**10.5.1.a**Examine documentation to verify that the<br>following is defined:<br>•<br>Audit log retention policies.<br>•<br>Procedures for retaining audit log history for at<br>least 12 months, with at least the most recent<br>three months immediately available online.|Retaining historical audit logs for at least 12<br>months is necessary because compromises often<br>go unnoticed for significant lengths of time.<br>Having centrally stored log history allows<br>investigators to better determine the length of<br>time a potential breach was occurring, and the<br>possible system(s) impacted. By having three<br>months of logs immediately available, an entity|
||**10.5.1.b**Examine configurations of audit log<br>history, interview personnel and examine audit logs<br>to verify that audit logs history is retained for at<br>least 12 months.<br>**10.5.1.c**Interview personnel and observe<br>processes to verify that at least the most recent|can quickly identify and minimize impact of a data<br>breach.<br>**Examples**<br>Methods that allow logs to be immediately<br>available include storing logs online, archiving<br>logs, or restoring logs quickly from backups.|
|**Customized Approach Objective**|three months’ audit log history is immediately<br>available for analysis.||
|Historical records of activity are available<br>immediately to support incident response and are<br>retained for at least 12 months.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 252_ 



###### **Requirements and Testing Procedures Guidance** 

###### **10.6 Time-synchronization mechanisms support consistent time settings across all systems.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**10.6.1**System clocks and time are synchronized<br>using time-synchronization technology.<br>**Customized Approach Objective**<br>Common time is established across all systems.|**10.6.1**Examine system configuration settings to<br>verify that time-synchronization technology is<br>implemented and kept current.|Time synchronization technology is used to<br>synchronize clocks on multiple systems. When<br>clocks are not properly synchronized, it can be<br>difficult, if not impossible, to compare log files<br>from different systems and establish an exact<br>sequence of events, which is crucial for forensic<br>analysis following a breach.|
|**Applicability Notes**<br>Keeping time-synchronization technology current<br>includes managing vulnerabilities and patching the<br>technology according to PCI DSS Requirements<br>6.3.1 and 6.3.3.||For post-incident forensics teams, the accuracy<br>and consistency of time across all systems and<br>the time of each activity are critical in determining<br>how the systems were compromised.<br>**Examples**<br>Network Time Protocol (NTP) is one example of<br>time-synchronization technology.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 253_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**10.6.2**Systems are configured to the correct and<br>consistent time as follows:<br>•<br>One or more designated time servers are in use.<br>•<br>Only the designated central time server(s)<br>receives time from external sources.|**10.6.2**Examine system configuration settings for<br>acquiring, distributing, and storing the correct time<br>to verify the settings are configured in accordance<br>with all elements specified in this requirement.|Using reputable time servers is a critical<br>component of the time synchronization process.<br>Accepting time updates from specific, industry-<br>accepted external sources helps prevent a<br>malicious individual from changing time settings<br>on systems.|
|•<br>Time received from external sources is based on<br>International Atomic Time or Coordinated<br>Universal Time (UTC).||**Good Practice**<br>Another option to prevent unauthorized use of<br>internal time servers is to encrypt updates with a|
|•<br>The designated time server(s) accept time<br>updates only from specific industry-accepted<br>external sources.||symmetric key and create access control lists that<br>specify the IP addresses of client machines that<br>will be provided with the time updates.|
|•<br>Where there is more than one designated time<br>server, the time servers peer with one another to<br>keep accurate time.|||
|•<br>Internal systems receive time information only<br>from designated central time server(s).|||
|**Customized Approach Objective**|||
|The time on all systems is accurate and consistent.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 254_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**10.6.3**Time synchronization settings and data are<br>protected as follows:<br>•<br>Access to time data is restricted to only<br>personnel with a business need.|**10.6.3.a**Examine system configurations and time-<br>synchronization settings to verify that access to<br>time data is restricted to only personnel with a<br>business need.|Attackers will try to change time configurations to<br>hide their activity. Therefore, restricting the ability<br>to change or modify time synchronization<br>configurations or the system time to<br>administrators will lessen the probability of an|
|•<br>Any changes to time settings on critical systems<br>are logged, monitored, and reviewed.|**10.6.3.b**Examine system configurations and time<br>synchronization settings and logs and observe<br>processes to verify that any changes to time|attacker successfully changing time<br>configurations.|
|**Customized Approach Objective**|settings on critical systems are logged, monitored,<br>and reviewed.||
|System time settings cannot be modified by<br>unauthorized personnel.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 255_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **10.7 Failures of critical security control systems are detected, reported, and responded to promptly.** 

###### **Defined Approach Requirements Defined Approach Testing Procedures** 

**10.7.1** **_Additional requirement for service providers only:_** Failures of critical security control systems are detected, alerted, and addressed promptly, including but not limited to failure of the following critical security control systems: 

**10.7.1.a** **_Additional testing procedure for service provider assessments only:_** Examine documentation to verify that processes are defined for the prompt detection and addressing of failures of critical security control systems, including but not limited to failure of all elements specified in this requirement. 

- Network security controls. 

- IDS/IPS. 

- FIM. 

**10.7.1.b** **_Additional testing procedure for service provider assessments only:_** Observe detection and alerting processes and interview personnel to verify that failures of critical security control systems are detected and reported, and that failure of a critical security control results in the generation of an alert. 

- Anti-malware solutions. 

- Physical access controls. 

- Logical access controls. 

- Audit logging mechanisms. 

- Segmentation controls (if used). 

###### **Purpose** 

Without formal processes to detect and alert when critical security controls fail, failures may go undetected for extended periods and provide attackers ample time to compromise system components and steal account data from the CDE. 

###### **Good Practice** 

The specific types of failures may vary, depending on the function of the device system component and technology in use. Typical failures include a system ceasing to perform its security function or not functioning in its intended manner, such as a firewall erasing all its rules or going offline. 

###### **Customized Approach Objective** 

Failures in critical security control systems are promptly identified and addressed. 

###### **Applicability Notes** 

This requirement applies only when the entity being assessed is a service provider. _This requirement will be superseded by Requirement 10.7.2 as of 31 March 2025._ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 256_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**10.7.2**Failures of critical security control systems<br>are detected, alerted, and addressed promptly,<br>including but not limited to failure of the following<br>critical security control systems:<br>•<br>Network security controls.|**10.7.2.a**Examine documentation to verify that<br>processes are defined for the prompt detection and<br>addressing of failures of critical security control<br>systems, including but not limited to failure of all<br>elements specified in this requirement.|Without formal processes to detect and alert<br>when critical security controls fail, failures may go<br>undetected for extended periods and provide<br>attackers ample time to compromise system<br>components and steal account data from the<br>CDE.|
|•<br>IDS/IPS.|**10.7.2.b**Observe detection and alerting processes|**Good Practice**|
|•<br>Change-detection mechanisms.<br>•<br>Anti-malware solutions.<br>•<br>Physical access controls.<br>•<br>Logical access controls.|<br>and interview personnel to verify that failures of<br>critical security control systems are detected and<br>reported, and that failure of a critical security<br>control results in the generation of an alert.|The specific types of failures may vary, depending<br>on the function of the device system component<br>and technology in use. However, typical failures<br>include a system no longer performing its security<br>function or not functioning in its intended|
|•<br>Audit logging mechanisms.<br>•<br>Segmentation controls (if used)||manner—for example, a firewall erasing its rules<br>or going offline.|



- Segmentation controls (if used). 

- Audit log review mechanisms. 

- Automated security testing tools (if used). 

**Customized Approach Objective** Failures in critical security control systems are promptly identified and addressed. **Applicability Notes** _This requirement applies to all entities, including service providers, and will supersede Requirement 10.7.1 as of 31 March 2025. It includes two additional critical security control systems not in Requirement 10.7.1. This requirement is a best practice until 31 March 2025, after which it will be required and must be fully considered during a PCI DSS assessment._ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 257_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**10.7.3**Failures of any critical security control<br>systems are responded to promptly, including but<br>not limited to:|**10.7.3.a**Examine documentation and interview<br>personnel to verify that processes are defined and<br>implemented to respond to a failure of any critical<br>|If alerts from failures of critical security control<br>systems are not responded to quickly and<br>effectively, attackers may use this time to insert<br>malicious software, gain control of a system, or|
|•<br>Restoring security functions.<br>•<br>Identifying and documenting the duration (date|security control system and include at least all<br>elements specified in this requirement.|steal data from the entity’s environment.<br>**Good Practice**|
|and time from start to end) of the security failure.<br>•<br>Identifying and documenting the cause(s) of<br>failure and documenting required remediation.|**10.7.3.b**Examine records to verify that failures of<br>critical security control systems are documented to<br>include:|Documented evidence (for example, records<br>within a problem management system) should<br>provide support that processes and procedures<br>|
|•<br>Identifying and addressing any security issues<br>that arose during the failure.<br>•<br>Determining whether further actions are required<br>as a result of the security failure.|•<br>Identification of cause(s) of the failure.<br>•<br>Duration (date and time start and end) of the<br>security failure.<br>•<br>Details of the remediation required to address|are in place to respond to security failures. In<br>addition, personnel should be aware of their<br>responsibilities in the event of a failure. Actions<br>and responses to the failure should be captured in<br>the documented evidence.|



   - Details of the remediation required to address the root cause. 

- Implementing controls to prevent the cause of failure from reoccurring. 

- Resuming monitoring of security controls. 

###### **Customized Approach Objective** 

Failures of critical security control systems are analyzed, contained, and resolved, and security controls restored to minimize impact. Resulting security issues are addressed, and measures taken to prevent reoccurrence. _(continued on next page)_ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 258_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Applicability Notes**||
|This requirement applies only when the entity being<br>assessed is a service provider until 31 March 2025,<br>after which this requirement will apply to all entities.||
|_This is a current v3.2.1 requirement that applies to_<br>_service providers only. However, this requirement is_||
|_a best practice for all other entities until 31 March_<br>_2025, after which it will be required and must be_||
|_fully considered during a PCI DSS assessment_.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 259_ 



#### **_Requirement 11: Test Security of Systems and Networks Regularly_** 

**Sections** 

- **11.1** Processes and mechanisms for regularly testing security of systems and networks are defined and understood. 

- **11.2** Wireless access points are identified and monitored, and unauthorized wireless access points are addressed. 

- **11.3** External and internal vulnerabilities are regularly identified, prioritized, and addressed. 

- **11.4** External and internal penetration testing is regularly performed, and exploitable vulnerabilities and security weaknesses are corrected. 

- **11.5** Network intrusions and unexpected file changes are detected and responded to. 

- **11.6** Unauthorized changes on payment pages are detected and responded to. 

**Overview** 

Vulnerabilities are being discovered continually by malicious individuals and researchers, as well as being introduced by new software. System components, processes, and bespoke and custom software should be tested frequently to ensure security controls continue to reflect a changing environment. 

Refer to _Appendix G_ for definitions of PCI DSS terms. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 260_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **11.1 Processes and mechanisms for regularly testing security of systems and networks are defined and understood.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**11.1.1**All security policies and operational<br>procedures that are identified in Requirement 11<br>are:<br>•<br>Documented.<br>•<br>Kept up to date.<br>•<br>In use.<br>•<br>Known to all affected parties.|**11.1.1**Examine documentation and interview<br>personnel to verify that security policies and<br>operational procedures are managed in<br>accordance with all elements specified in this<br>requirement.|Requirement 11.1.1 is about effectively managing<br>and maintaining the various policies and<br>procedures specified throughout Requirement 11.<br>While it is important to define the specific policies<br>or procedures called out in Requirement 11, it is<br>equally important to ensure they are properly<br>documented, maintained, and disseminated.<br>**Good Practice**<br>It is important to update policies and procedures|
|**Customized Approach Objective**||as needed to address changes in processes,<br>technologies, and business objectives. For this|
|Expectations, controls, and oversight for meeting<br>activities within Requirement 11 are defined and<br>adhered to by affected personnel. All supporting<br>activities are repeatable, consistently applied, and<br>conform to management’s intent.||reason, consider updating these documents as<br>soon as possible after a change occurs and not<br>only on a periodic cycle.<br>**Definitions**<br>Security policies define the entity’s security<br>objectives and principles. Operational procedures<br>describe how to perform activities, and define the<br>controls, methods, and processes that are<br>followed to achieve the desired result in a<br>consistent manner and in accordance with policy<br>objectives.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 261_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**11.1.2**Roles and responsibilities for performing<br>activities in Requirement 11 are documented,<br>assigned, and understood.|**11.1.2.a**Examine documentation to verify that<br>descriptions of roles and responsibilities for<br>performing activities in Requirement 11 are<br>documented and assigned.|If roles and responsibilities are not formally<br>assigned, personnel may not be aware of their<br>day-to-day responsibilities and critical activities<br>may not occur.<br>**Good Practice**|
|**Customized Approach Objective**<br>Day-to-day responsibilities for performing all the<br>activities in Requirement 11 are allocated.<br>Personnel are accountable for successful,<br>continuous operation of these requirements.|**11.1.2.b**Interview personnel with responsibility for<br>performing activities in Requirement 11 to verify<br>that roles and responsibilities are assigned as<br>documented and are understood.|Roles and responsibilities may be documented<br>within policies and procedures or maintained<br>within separate documents.<br>As part of communicating roles and<br>responsibilities, entities can consider having<br>personnel acknowledge their acceptance and<br>understanding of their assigned roles and<br>responsibilities.<br>**Examples**<br>A method to document roles and responsibilities<br>is a responsibility assignment matrix that includes<br>who is responsible, accountable, consulted, and<br>informed (also called a RACI matrix).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 262_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **11.2 Wireless access points are identified and monitored, and unauthorized wireless access points are addressed.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**11.2.1**Authorized and unauthorized wireless access<br>points are managed as follows:<br>•<br>The presence of wireless (Wi-Fi) access points<br>is tested for,|**11.2.1.a**Examine policies and procedures to verify<br>processes are defined for managing both<br>authorized and unauthorized wireless access<br>points with all elements specified in this<br>|Implementation and/or exploitation of wireless<br>technology within a network are common paths<br>for malicious users to gain unauthorized access to<br>the network and cardholder data. Unauthorized<br>wireless devices could be hidden within or|
|•<br>All authorized and unauthorized wireless access|requirement.|attached to a computer or other system<br>|
|points are detected and identified,<br>•<br>Testing, detection, and identification occurs at<br>least once every three months.<br>•<br>If automated monitoring is used, personnel are<br>notified via generated alerts.|**11.2.1.b**Examine the methodology(ies) in use and<br>the resulting documentation, and interview<br>personnel to verify processes are defined to detect<br>and identify both authorized and unauthorized<br>wireless access points in accordance with all<br>elements specified in this requirement.|component. These devices could also be<br>attached directly to a network port, to a network<br>device such as a switch or router, or inserted as a<br>wireless interface card inside a system<br>component.<br>Even if a company has a policy prohibiting the<br>use of wireless technologies, an unauthorized|
||**11.2.1.c**Examine wireless assessment results and<br>interview personnel to verify that wireless<br>assessments were conducted in accordance with<br>all elements specified in this requirement.|wireless device or network could be installed<br>without the company’s knowledge, allowing an<br>attacker to enter the network easily and “invisibly.”<br>Detecting and removing such unauthorized<br>access points reduces the duration and likelihood|
||**11.2.1.d**If automated monitoring is used, examine<br>configuration settings to verify the configuration will|of such devices being leveraged for an attack.|
|**Customized Approach Objective**|generate alerts to notify personnel.|_(continued on next page)_|
|Unauthorized wireless access points are identified<br>and addressed periodically.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 263_ 



###### **Requirements and Testing Procedures Guidance** 

|**Applicability Notes**|**Good Practice**|
|---|---|
|The requirement applies even when a policy exists<br>that prohibits the use of wireless technology.|The size and complexity of an environment will<br>dictate the appropriate tools and processes to be<br>used to provide sufficient assurance that a rogue|
|Methods used to meet this requirement must be<br>sufficient to detect and identify both authorized and<br>unauthorized devices, including unauthorized<br>devices attached to devices that themselves are<br>authorized.|wireless access point has not been installed in the<br>environment.<br>For example, performing a detailed physical<br>inspection of a single stand-alone retail kiosk in a<br>shopping mall, where all communication<br>components are contained within tamper-resistant<br>and tamper-evident casings, may be sufficient to<br>provide assurance that a rogue wireless access<br>point has not been attached or installed.<br>However, in an environment with multiple nodes<br>(such as in a large retail store, call center, server<br>room or data center), detailed physical inspection<br>can be difficult. In this case, multiple methods<br>may be combined, such as performing physical<br>system inspections in conjunction with the results<br>of a wireless analyzer.<br>**Definitions**|
||This is also referred to as rogue access point<br>detection.<br>**Examples**<br>Methods that may be used include but are not<br>limited to wireless network scans, physical/logical<br>inspections of system components and<br>infrastructure, network access control (NAC), or<br>wireless IDS/IPS. NAC and wireless IDS/IPS are<br>examples of automated monitoring tools.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 264_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**11.2.2**An inventory of authorized wireless access<br>points is maintained, including a documented<br>business justification.|**11.2.2**Examine documentation to verify that an<br>inventory of authorized wireless access points is<br>maintained, and a business justification is<br>documented for all authorized wireless access<br>it|An inventory of authorized wireless access points<br>can help administrators quickly respond when<br>unauthorized wireless access points are detected.<br>This helps to proactively minimize the exposure of<br>CDE to malicious individuals.|
|**Customized Approach Objective**|pons.|**Good Practice**<br>If using a wireless scanner, it is equally important|
|Unauthorized wireless access points are not<br>mistaken for authorized wireless access points.||to have a defined list of known access points<br>which, while not attached to the company’s<br>network, will usually be detected during a scan.<br>These non-company devices are often found in<br>multi-tenant buildings or businesses located near<br>one another. However, it is important to verify that<br>these devices are not connected to the entity’s<br>network port or through another network-<br>connected device and given an SSID resembling<br>a nearby business. Scan results should note such<br>devices and how it was determined that these<br>devices could be “ignored.” In addition, detection<br>of any unauthorized wireless access points that<br>are determined to be a threat to the CDE should<br>be managed following the entity’s incident<br>response plan per Requirement 12.10.1.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 265_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **11.3 External and internal vulnerabilities are regularly identified, prioritized, and addressed.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**11.3.1**Internal vulnerability scans are performed as<br>follows:<br>•<br>At least once every three months.<br>•<br>Vulnerabilities that are either high-risk or critical<br>(according to the entity’s vulnerability risk<br>rankings defined at Requirement 6.3.1) are<br>resolved.<br>•<br>Rescans are performed that confirm all high-risk<br>and all critical vulnerabilities (as noted above)<br>have been resolved.|**11.3.1.a**Examine internal scan report results from<br>the last 12 months to verify that internal scans<br>occurred at least once every three months in the<br>most recent 12-month period.<br>**11.3.1.b**Examine internal scan report results from<br>each scan and rescan run in the last 12 months to<br>verify that all high-risk vulnerabilities and all critical<br>vulnerabilities (defined in PCI DSS Requirement<br>6.3.1) are resolved.|Identifying and addressing vulnerabilities promptly<br>reduces the likelihood of a vulnerability being<br>exploited and the potential compromise of a<br>system component or cardholder data.<br>Vulnerability scans conducted at least every three<br>months provide this detection and identification.<br>**Good Practice**<br>Vulnerabilities posing the greatest risk to the<br>environment (for example, ranked high or critical<br>per Requirement 6.3.1) should be resolved with<br>the highest priority. Vulnerabilities identified|
|•<br>Scan tool is kept up to date with latest<br>vulnerability information.<br>•<br>Scans are performed by qualified personnel and<br>organizational independence of the tester exists.|**11.3.1.c**Examine scan tool configurations and<br>interview personnel to verify that the scan tool is<br>kept up to date with the latest vulnerability<br>information.<br>**11.3.1.d**Interview responsible personnel to verify<br>that the scan was performed by a qualified internal<br>resource(s) or qualified external third party and that<br>organizational independence of the tester exists.|during internal vulnerability scans should be part<br>of a vulnerability management process that<br>includes multiple vulnerability sources, as<br>specified in Requirement 6.3.1.<br>Multiple scan reports can be combined for the<br>quarterly scan process to show that all systems<br>were scanned and all applicable vulnerabilities<br>were resolved as part of the three-month<br>vulnerability scan cycle. However, additional<br>documentation may be required to verify non-|
|**Customized Approach Objective**||remediated vulnerabilities are in the process of<br>being resolved.|
|The security posture of all system components is<br>verified periodically using automated tools designed<br>to detect vulnerabilities operating inside the<br>network. Detected vulnerabilities are assessed and<br>rectified based on a formal risk assessment<br>framework.||While scans are required at least once every<br>three months, more frequent scans are<br>recommended depending on the network<br>complexity, frequency of change, and types of<br>devices, software, and operating systems used.|
|_(continued on next page)_||_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 266_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Applicability Notes**|**Definitions**|
|It is not required to use a QSA or ASV to conduct<br>internal vulnerability scans.|A vulnerability scan is a combination of<br>automated tools, techniques, and/or methods run<br>against external and internal devices and servers,|
|Internal vulnerability scans can be performed by<br>qualified, internal staff that are reasonably<br>independent of the system component(s) being<br>scanned (for example, a network administrator<br>should not be responsible for scanning the network),<br>or an entity may choose to have internal<br>vulnerability scans performed by a firm specializing<br>in vulnerability scanning.|designed to expose potential vulnerabilities in<br>applications, operating systems, and network<br>devices that could be found and exploited by<br>malicious individuals.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 267_ 



###### **Requirements and Testing Procedures** 

**Defined Approach Requirements Defined Approach Testing Procedures 11.3.1.1** All other applicable vulnerabilities (those **11.3.1.1.a** Examine the entity’s targeted risk not ranked as high-risk vulnerabilities or critical analysis that defines the risk for addressing all vulnerabilities according to the entity’s vulnerability other applicable vulnerabilities (those not ranked risk rankings defined at Requirement 6.3.1) are as high-risk vulnerabilities or critical vulnerabilities managed as follows: according to the entity’s vulnerability risk rankings • Addressed based on the risk defined in the at Requirement 6.3.1) to verify the risk analysis was performed in accordance with all elements entity’s targeted risk analysis, which is specified at Requirement 12.3.1. performed according to all elements specified in Requirement 12.3.1. **11.3.1.1.b** Interview responsible personnel and • Rescans are conducted as needed. examine internal scan report results or other documentation to verify that all other applicable vulnerabilities (those not ranked as high-risk vulnerabilities or critical vulnerabilities according to the entity’s vulnerability risk rankings at **Customized Approach Objective** Requirement 6.3.1) are addressed based on the risk defined in the entity’s targeted risk analysis, Lower ranked vulnerabilities (lower than high-risk or and that the scan process includes rescans as critical) are addressed at a frequency in accordance needed to confirm the vulnerabilities have been with the entity’s risk. addressed. **Applicability Notes** The timeframe for addressing lower-risk vulnerabilities is subject to the results of a risk analysis per Requirement 12.3.1 that includes (minimally) identification of assets being protected, threats, and likelihood and/or impact of a threat being realized. _This requirement is a best practice until 31 March 2025, after which it will be required and must be fully considered during a PCI DSS assessment._ 

###### **Guidance** 

###### **Purpose** 

All vulnerabilities, regardless of criticality, provide a potential avenue of attack and must therefore be addressed periodically, with the vulnerabilities that expose the most risk addressed more quickly to limit the potential window of attack. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 268_ 



###### **Requirements and Testing Procedures** 

- **Defined Approach Requirements 11.3.1.2** Internal vulnerability scans are performed via authenticated scanning as follows: 

**Defined Approach Testing Procedures 11.3.1.2.a** Examine scan tool configurations to verify that authenticated scanning is used for internal scans, with sufficient privileges, for those systems that accept credentials for scanning. **11.3.1.2.b** Examine scan report results and interview personnel to verify that authenticated scans are performed. 

- Systems that are unable to accept credentials for authenticated scanning are documented. 

- Sufficient privileges are used for those systems that accept credentials for scanning. 

- If accounts used for authenticated scanning can be used for interactive login, they are managed in accordance with Requirement 8.2.2. 

**11.3.1.2.c** If accounts used for authenticated scanning can be used for interactive login, examine the accounts and interview personnel to **Customized Approach Objective** verify the accounts are managed following all elements specified in Requirement 8.2.2. 

Automated tools used to detect vulnerabilities can detect vulnerabilities local to each system, which are not visible remotely. 

are not visible remotely. **11.3.1.2.d** Examine documentation to verify that systems that are unable to accept credentials for **Applicability Notes** authenticated scanning are defined. 

###### **Guidance** 

###### **Purpose** 

Authenticated scanning provides greater insight into an entity’s vulnerability landscape since it can detect vulnerabilities that unauthenticated scans cannot detect. Attackers may leverage vulnerabilities that an entity is unaware of because certain vulnerabilities will only be detected with authenticated scanning. 

Authenticated scanning can yield significant additional information about an organization’s vulnerabilities. 

###### **Good Practice** 

The credentials used for these scans should be considered highly privileged. They should be protected and controlled as such, following PCI DSS Requirements 7 and 8 (except for those requirements for multi-factor authentication and application and system accounts). 

The authenticated scanning tools can be either host-based or network-based. “Sufficient” privileges are those needed to access system resources such that a thorough scan can be conducted that detects known vulnerabilities. This requirement does not apply to system components that cannot accept credentials for scanning. Examples of systems that may not accept credentials for scanning include some network and security appliances, mainframes, and containers. _This requirement is a best practice until 31 March 2025, after which it will be required and must be fully considered during a PCI DSS assessment._ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 269_ 



###### **Requirements and Testing Procedures Guidance** 

**Defined Approach Requirements Defined Approach Testing Procedures Purpose** Scanning an environment after any significant **11.3.1.3** Internal vulnerability scans are performed **11.3.1.3.a** Examine change control documentation changes ensures that changes were completed after any significant change as follows: and internal scan reports to verify that system appropriately such that the security of the • Vulnerabilities that are either high-risk or critical components were scanned after any significant environment was not compromised because of (according to the entity’s vulnerability risk changes. the change. rankings defined at Requirement 6.3.1) are **Good Practice** resolved. **11.3.1.3.b** Interview personnel and examine • Rescans are conducted as needed. internal scan and rescan reports to verify that Entities should perform scans after significant internal scans were performed after significant changes as part of the change process per • Scans are performed by qualified personnel and changes and that all high-risk vulnerabilities and all Requirement 6.5.2 and before considering the organizational independence of the tester exists critical vulnerabilities (defined in PCI DSS change complete. All system components (not required to be a QSA or ASV). Requirement 6.3.1) were resolved. affected by the change will need to be scanned. **11.3.1.3.c** Interview personnel to verify that internal scans are performed by a qualified internal **Customized Approach Objective** resource(s) or qualified external third party and that organizational independence of the tester exists. The security posture of all system components is verified following significant changes to the network or systems, by using automated tools designed to detect vulnerabilities operating inside the network. Detected vulnerabilities are assessed and rectified based on a formal risk assessment framework. **Applicability Notes** Authenticated internal vulnerability scanning per Requirement 11.3.1.2 is not required for scans performed after significant changes. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 270_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

**Defined Approach Requirements Defined Approach Testing Procedures Purpose** Attackers routinely look for unpatched or **11.3.2** External vulnerability scans are performed as **11.3.2.a** Examine ASV scan reports from the last vulnerable externally facing servers, which can be follows: 12 months to verify that external vulnerability scans leveraged to launch a directed attack. • At least once every three months. occurred at least once every three months in the Organizations must ensure these externally facing most recent 12-month period. • By a PCI SSC Approved Scanning Vendor devices are regularly scanned for weaknesses (ASV). and that vulnerabilities are patched or remediated **11.3.2.b** Examine the ASV scan report from each • Vulnerabilities are resolved and _ASV Program_ to protect the entity. scan and rescan run in the last 12 months to verify _Guide_ requirements for a passing scan are met. that vulnerabilities are resolved and the _ASV_ Because external networks are at greater risk of • Rescans are performed as needed to confirm _Program Guide_ requirements for a passing scan compromise, external vulnerability scanning must be performed at least once every three months by that vulnerabilities are resolved per the _ASV_ are met. a PCI SSC Approved Scanning Vendor (ASV). _Program Guide_ requirements for a passing scan. **11.3.2.c** Examine the ASV scan reports to verify **Good Practice** that the scans were completed by a PCI SSC While scans are required at least once every **Customized Approach Objective** Approved Scanning Vendor (ASV). three months, more frequent scans are recommended depending on the network This requirement is not eligible for the customized complexity, frequency of change, and types of approach. devices, software, and operating systems used. Vulnerabilities identified during external **Applicability Notes** vulnerability scans should be part of a vulnerability management process that includes For the initial PCI DSS assessment against this multiple vulnerability sources, as specified in requirement, it is not required that four passing Requirement 6.3.1. scans be completed within 12 months if the Multiple scan reports can be combined to show assessor verifies: 1) the most recent scan result was that all systems were scanned and that all a passing scan, 2) the entity has documented applicable vulnerabilities were resolved as part of policies and procedures requiring scanning at least the three-month vulnerability scan cycle. once every three months, and 3) vulnerabilities However, additional documentation may be noted in the scan results have been corrected as required to verify non-remediated vulnerabilities shown in a re-scan(s). are in the process of being resolved. 

For the initial PCI DSS assessment against this requirement, it is not required that four passing scans be completed within 12 months if the assessor verifies: 1) the most recent scan result was a passing scan, 2) the entity has documented policies and procedures requiring scanning at least once every three months, and 3) vulnerabilities noted in the scan results have been corrected as shown in a re-scan(s). _(continued on next page)_ 

###### **Further Information** 

See the _ASV Program Guide_ on the PCI SSC website. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 271_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|However, for subsequent years after the initial PCI<br>DSS assessment, passing scans at least every three<br>months must have occurred.||
|ASV scanning tools can scan a vast array of<br>network types and topologies. Any specifics about<br>the target environment (for example, load balancers,<br>third-party providers, ISPs, specific configurations,<br>protocols in use, scan interference) should be<br>worked out between the ASV and scan customer.||
|Refer to the_ASV Program Guide_published on the<br>PCI SSC website for scan customer responsibilities,<br>scan preparation, etc.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 272_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**11.3.2.1**External vulnerability scans are performed<br>after any significant change as follows:<br>•<br>Vulnerabilities that are scored 4.0 or higher by<br>the CVSS are resolved.|**11.3.2.1.a**Examine change control documentation<br>and external scan reports to verify that system<br>components were scanned after any significant<br>changes.|Scanning an environment after any significant<br>changes ensures that changes were completed<br>appropriately such that the security of the<br>environment was not compromised because of<br>the change.|
|•<br>Rescans are conducted as needed.<br>•<br>Scans are performed by qualified personnel and<br>organizational independence of the tester exists<br>(not required to be a QSA or ASV).|**11.3.2.1.b**Interview personnel and examine<br>external scan and rescan reports to verify that<br>external scans were performed after significant<br>changes and that vulnerabilities scored 4.0 or<br>higher by the CVSS were resolved.|**Good Practice**<br>Entities should include the need to perform scans<br>after significant changes as part of the change<br>process and before the change is considered<br>complete. All system components affected by the<br>change will need to be scanned.|
||**11.3.2.1.c**Interview personnel to verify that<br>external scans are performed by a qualified||
|**Customized Approach Objective**|internal resource(s) or qualified external third party<br>and that organizational independence of the tester||
|The security posture of all system components is<br>verified following significant changes to the network<br>or systems, by using tools designed to detect<br>vulnerabilities operating from outside the network.<br>Detected vulnerabilities are assessed and rectified<br>based on a formal risk assessment framework.|exists.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 273_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

**11.4 External and internal penetration testing is regularly performed, and exploitable vulnerabilities and security weaknesses are corrected.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**11.4.1**A penetration testing methodology is defined,<br>documented, and implemented by the entity, and<br>includes:|**11.4.1**Examine documentation and interview<br>personnel to verify that the penetration-testing<br>methodology defined, documented, and<br>|Attackers spend a lot of time finding external and<br>internal vulnerabilities to leverage to obtain<br>access to cardholder data and then to exfiltrate<br>that data. As such, entities need to test their|
|•<br>Industry-accepted penetration testing<br>approaches.|implemented by the entity includes all elements<br>specified in this requirement.|networks thoroughly, just as an attacker would do.<br>This testing allows the entity to identify and|
|•<br>Coverage for the entire CDE perimeter and<br>critical systems.||remediate weakness that might be leveraged to<br>compromise the entity’s network and data, and<br>|
|•<br>Testing from both inside and outside the<br>network.||then to take appropriate actions to protect the<br>network and system components from such<br>attacks.|
|•<br>Testing to validate any segmentation and scope-<br>reduction controls.||<br>**Good Practice**|
|•<br>Application-layer penetration testing to identify,<br>at a minimum, the vulnerabilities listed in<br>Requirement 6.2.4.||Penetration testing techniques will differ based on<br>an organization’s needs and structure and should<br>be suitable for the tested environment—for<br>example, fuzzing, injection, and forgery tests|
|•<br>Network-layer penetration tests that encompass<br>all components that support network functions<br>as well as operating systems.||<br>might be appropriate. The type, depth, and<br>complexity of the testing will depend on the<br>specific environment and the needs of the|
|•<br>Review and consideration of threats and<br>vulnerabilities experienced in the last 12 months.||organization.<br>**Definitions**|
|•<br>Documented approach to assessing and<br>addressing the risk posed by exploitable<br>vulnerabilities and security weaknesses found<br>during penetration testing.||Penetration tests simulate a real-world attack<br>situation intending to identify how far an attacker<br>could penetrate an environment, given differing<br>amounts of information provided to the tester.|
|•<br>Retention of penetration testing results and<br>remediation activities results for at least 12<br>months.||This allows an entity to better understand its<br>potential exposure and develop a strategy to<br>defend against attacks. A penetration test differs<br>from a vulnerability scan, as a penetration test is<br>an active process that usually includes exploiting<br>identified vulnerabilities.|
|||_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 274_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Customized Approach Objective**<br>A formal methodology is defined for thorough<br>technical testing that attempts to exploit<br>vulnerabilities and security weaknesses via|Scanning for vulnerabilities alone is not a<br>penetration test, nor is a penetration test<br>adequate if the focus is solely on trying to exploit<br>vulnerabilities found in a vulnerability scan.<br>Conducting a vulnerability scan may be one of the|
|simulated attack methods by a competent manual<br>attacker.|first steps, but it is not the only step a penetration<br>tester will perform to plan the testing strategy.<br>Even if a vulnerability scan does not detect known|
|**Applicability Notes**<br>Testing from inside the network (or “internal|vulnerabilities, the penetration tester will often<br>gain enough knowledge about the system to<br>identify possible security gaps.|
|penetration testing”) means testing from both inside<br>the CDE and into the CDE from trusted and<br>untrusted internal networks.<br>Testing from outside the network (or “external<br>penetration testing”) means testing the exposed<br>external perimeter of trusted networks, and critical<br>systems connected to or accessible to public<br>network infrastructures.|Penetration testing is a highly manual process.<br>While some automated tools may be used, the<br>tester uses their knowledge of systems to gain<br>access into an environment. Often the tester will<br>chain several types of exploits together with the<br>goal of breaking through layers of defenses. For<br>example, if the tester finds a way to gain access<br>to an application server, the tester will then use<br>the compromised server as a point to stage a new<br>attack based on the resources to which the server<br>has access. In this way, a tester can simulate the<br>techniques used by an attacker to identify areas<br>of potential weakness in the environment. The<br>testing of security monitoring and detection<br>methods—for example, to confirm the<br>effectiveness of logging and file integrity<br>monitoring mechanisms, should also be<br>considered.|
||_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 275_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**11.4.1**_(continued)_||**Further Information**<br>Refer to the_Information Supplement: Penetration_<br>_Testing Guidance_for additional guidance.<br>Industry-accepted penetration testing approaches<br>include:<br>_The Open Source Security Testing Methodology_<br>_and Manual (OSSTMM)_<br>_Open Web Application Security Project (OWASP)_<br>_penetration testing programs._|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**11.4.2**Internal penetration testing is performed:<br>•<br>Per the entity’s defined methodology,<br>•<br>At least once every 12 months<br>•<br>After any significant infrastructure or application<br>upgrade or change|**11.4.2.a**Examine the scope of work and results<br>from the most recent internal penetration test to<br>verify that penetration testing is performed in<br>accordance with all elements specified in this<br>requirement.|Internal penetration testing serves two purposes.<br>Firstly, just like an external penetration test, it<br>discovers vulnerabilities and misconfigurations<br>that could be used by an attacker that had<br>managed to get some degree of access to the<br>internal network, whether that is because the<br>|
|•<br>By a qualified internal resource or qualified<br>external third-party<br>•<br>Organizational independence of the tester exists<br>(not required to be a QSA or ASV).|**11.4.2.b**Interview personnel to verify that the<br>internal penetration test was performed by a<br>qualified internal resource or qualified external<br>third-party and that organizational independence of<br>the tester exists (not required to be a QSA or<br>ASV)|attacker is an authorized user conducting<br>unauthorized activities, or an external attacker<br>that had managed to penetrate the entity’s<br>perimeter.<br>Secondly, internal penetration testing also helps<br>entities to discover where their change control|
|**Customized Approach Objective**|.|process failed by detecting previously unknown<br>systems. Additionally, it verifies the status of|
|Internal system defenses are verified by technical<br>testing according to the entity’s defined<br>methodology as frequently as needed to address<br>evolving and new attacks and threats and ensure<br>that significant changes do not introduce unknown<br>vulnerabilities.||many of the controls operating within the CDE.<br>A penetration test is not truly a “test” because the<br>outcome of a penetration test is not something<br>that can be classified as a “pass” or a “fail.” The<br>best outcome of a test is a catalog of<br>vulnerabilities and misconfigurations that an entity|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 276_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|did not know about, and the penetration tester<br>found them before an attacker could. A|
|**11.4.3**External penetration testing is performed:<br>•<br>Per the entity’s defined methodology<br>•<br>At least once every 12 months<br>•<br>After any significant infrastructure or application<br>upgrade or change|**11.4.3.a**Examine the scope of work and results<br>from the most recent external penetration test to<br>verify that penetration testing is performed<br>according to all elements specified in this<br>requirement.|penetration test that found nothing is typically<br>indicative of shortcomings of the penetration<br>tester, rather than being a positive reflection of<br>the security posture of the entity.<br>**Good Practice**<br>S idi h hi  lifid|
|•<br>By a qualified internal resource or qualified<br>external third party<br>•<br>Organizational independence of the tester exists<br>(not required to be a QSA or ASV)|**11.4.3.b**Interview personnel to verify that the<br>external penetration test was performed by a<br>qualified internal resource or qualified external third<br>party and that organizational independence of the<br>tester exists (not required to be a QSA or ASV).|ome conseratons wen coosng a quae<br>resource to perform penetration testing include:<br>•<br>Specific penetration testing certifications,<br>which may be an indication of the tester’s skill<br>level and competence.<br>•<br>Prior experience conducting penetration|
|**Customized Approach Objective**||testing—for example, the number of years of<br>experience, and the type and scope of prior|
|External system defenses are verified by technical<br>testing according to the entity’s defined<br>methodology as frequently as needed to address<br>evolving and new attacks and threats, and to ensure<br>that significant changes do not introduce unknown<br>vulnerabilities.||engagements can help confirm whether the<br>tester’s experience is appropriate for the<br>needs of the engagement.<br>**Further Information**<br>Refer to the_Information Supplement: Penetration_<br>_Testing Guidance_on the PCI SSC website for<br>additional guidance.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 277_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**11.4.4**Exploitable vulnerabilities and security<br>weaknesses found during penetration testing are<br>corrected as follows:<br>•<br>In accordance with the entity’s assessment of<br>the risk posed by the security issue as defined in<br>Requirement 6.3.1.<br>•<br>Penetration testing is repeated to verify the<br>corrections.|**11.4.4**Examine penetration testing results to verify<br>that noted exploitable vulnerabilities and security<br>weaknesses were corrected in accordance with all<br>elements specified in this requirement.|The results of a penetration test are usually a<br>prioritized list of vulnerabilities discovered by the<br>exercise. Often a tester will have chained a<br>number of vulnerabilities together to compromise<br>a system component. Remediating the<br>vulnerabilities found by a penetration test<br>significantly reduces the probability that the same<br>vulnerabilities will be exploited by a malicious<br>attacker.<br>Using the entity’s own vulnerability risk|
|**Customized Approach Objective**||assessment process (see requirement 6.3.1)<br>ensures that the vulnerabilities that pose the|
|Vulnerabilities and security weaknesses found while<br>verifying system defenses are mitigated.||highest risk to the entity will be remediated more<br>quickly.<br>**Good Practice**<br>As part of the entity’s assessment of risk, entities<br>should consider how likely the vulnerability is to<br>be exploited and whether there are other controls<br>present in the environment to reduce the risk.<br>Any weaknesses that point to PCI DSS<br>requirements not being met should be addressed.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 278_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

**Defined Approach Requirements Defined Approach Testing Procedures Purpose** When an entity uses segmentation controls to **11.4.5** If segmentation is used to isolate the CDE **11.4.5.a** Examine segmentation controls and isolate the CDE from internal untrusted networks, from other networks, penetration tests are review penetration-testing methodology to verify the security of the CDE is dependent on that performed on segmentation controls as follows: that penetration-testing procedures are defined to segmentation functioning. Many attacks have • At least once every 12 months and after any test all segmentation methods in accordance with involved the attacker moving laterally from what changes to segmentation controls/methods all elements specified in this requirement. an entity deemed an isolated network into the • Covering all segmentation controls/methods in CDE. Using penetration testing tools and **11.4.5.b** Examine the results from the most recent use. techniques to validate that an untrusted network penetration test to verify the penetration test is indeed isolated from the CDE can alert the • According to the entity’s defined penetration covers and addresses all elements specified in this entity to a failure or misconfiguration of the testing methodology. requirement. segmentation controls, which can then be • Confirming that the segmentation rectified. controls/methods are operational and effective, **11.4.5.c** Interview personnel to verify that the test **Good Practice** and isolate the CDE from all out-of-scope was performed by a qualified internal resource or systems. qualified external third party and that organizational Techniques such as host discovery and port • Confirming effectiveness of any use of isolation independence of the tester exists (not required to scanning can be used to verify out-of-scope segments have no access to the CDE. to separate systems with differing security levels be a QSA or ASV). 

- Confirming effectiveness of any use of isolation to separate systems with differing security levels (see Requirement 2.2.3). 

- Performed by a qualified internal resource or qualified external third party. 

- Organizational independence of the tester exists (not required to be a QSA or ASV). 

###### **Customized Approach Objective** 

If segmentation is used, it is verified periodically by technical testing to be continually effective, including after any changes, in isolating the CDE from all outof-scope systems. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 279_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**11.4.6** **_Additional requirement for service_**<br>**_providers only:_**If segmentation is used to isolate<br>the CDE from other networks, penetration tests are<br>performed on segmentation controls as follows:<br><br>At least once every six months and after any<br>|**11.4.6.a** **_Additional testing procedure for_**<br>**_service provider assessments only:_**Examine<br>the results from the most recent penetration test to<br>verify that the penetration covers and addressed all<br>elements specified in this requirement.|Service providers typically have access to greater<br>volumes of cardholder data or can provide an<br>entry point that can be exploited to then<br>compromise multiple other entities. Service<br>providers also typically have larger and more<br>complex networks that are subject to more|
|changes to segmentation controls/methods.||frequent change. The probability of segmentation|
|•<br>Covering all segmentation controls/methods in<br>use.<br>•<br>According to the entity’s defined penetration<br>testing methodology.<br>•<br>Confirming that the segmentation<br>controls/methods are operational and effective,<br>and isolate the CDE from all out-of-scope<br>systems.|**11.4.6.b** **_Additional testing procedure for_**<br>**_service provider assessments only:_ **Interview<br>personnel to verify that the test was performed by<br>a qualified internal resource or qualified external<br>third party and that organizational independence of<br>the tester exists (not required to be a QSA or<br>ASV).|controls failing in complex and dynamic networks<br>is greater in service-provider environments.<br>Validating segmentation controls more frequently<br>is likely to discover such failings before they can<br>be exploited by an attacker attempting to pivot<br>laterally from an out-of-scope untrusted network<br>to the CDE.<br>**Good Practice**|
|•<br>Confirming effectiveness of any use of isolation<br>to separate systems with differing security levels<br>(see Requirement 2.2.3).<br>•<br>Performed by a qualified internal resource or<br>qualified external third party.||Although the requirement specifies that this scope<br>validation is carried out at least once every six<br>months and after significant change, this exercise<br>should be performed as frequently as possible to<br>ensure it remains effective at isolating the CDE<br>from other networks.|



- At least once every six months and after any changes to segmentation controls/methods. 

- Organizational independence of the tester exists (not required to be a QSA or ASV). 

###### **Customized Approach Objective** 

If segmentation is used, it is verified by technical testing to be continually effective, including after any changes, in isolating the CDE from out-of-scope systems. 

###### **Applicability Notes** 

This requirement applies only when the entity being assessed is a service provider. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 280_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**11.4.7** **_Additional requirement for multi-tenant_**<br>**_service providers only:_**Multi-tenant service<br>providers support their customers for external<br>penetration testing per Requirement 11.4.3 and<br>11.4.4.|**11.4.7** **_Additional testing procedure for multi-_**<br>**_tenant service providers only:_**Examine evidence<br>to verify that multi-tenant service providers support<br>their customers for external penetration testing per<br>Requirement 11.4.3 and 11.4.4.|Entities need to conduct penetration tests in<br>accordance with PCI DSS to simulate attacker<br>behavior and discover vulnerabilities in their<br>environment. In shared and cloud environments,<br>the multi-tenant service provider may be<br>concerned about the activities of a penetration|
|**Customized Approach Objective**||tester affecting other customers’ systems.<br>Multi-tenant service providers cannot forbid|
|Multi-tenant service providers support their<br>customers’ need for technical testing either by<br>providing access or evidence that comparable<br>technical testing has been undertaken.<br>_(continued on next page)_||penetration testing because this would leave their<br>customers’ systems open to exploitation.<br>Therefore, multi-tenant service providers must<br>support customer requests to conduct penetration<br>testing or for penetration testing results.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 281_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Applicability Notes**||
|This requirement applies only when the entity being<br>assessed is a multi-tenant service provider.||
|To meet this requirement, a multi-tenant service<br>provider may either:||
|•<br>Provide evidence to its customers to show that<br>penetration testing has been performed<br>according to Requirements 11.4.3 and 11.4.4 on<br>the customers’ subscribed infrastructure, or||
|•<br>Provide prompt access to each of its customers,<br>so customers can perform their own penetration<br>testing.||
|Evidence provided to customers can include<br>redacted penetration testing results but needs to<br>include sufficient information to prove that all<br>elements of Requirements 11.4.3 and 11.4.4 have<br>been met on the customer’s behalf.||
|Refer also to_Appendix A1: Additional PCI DSS_<br>_Requirements for Multi-Tenant Service Providers_.||
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_||
|_fully considered during a PCI DSS assessment._||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 282_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **11.5 Network intrusions and unexpected file changes are detected and responded to.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|
|---|---|
|**11.5.1**Intrusion-detection and/or intrusion-<br>prevention techniques are used to detect and/or<br>prevent intrusions into the network as follows:|**11.5.1.a**Examine system configurations and<br>network diagrams to verify that intrusion-detection<br>and/or intrusion-prevention techniques are in place|
|All tffi i itd t th it f th|to monitor all traffic:|



|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**11.5.1**Intrusion-detection and/or intrusion-<br>prevention techniques are used to detect and/or<br>prevent intrusions into the network as follows:<br>•<br>All traffic is monitored at the perimeter of the<br>CDE.|**11.5.1.a**Examine system configurations and<br>network diagrams to verify that intrusion-detection<br>and/or intrusion-prevention techniques are in place<br>to monitor all traffic:<br>•<br>At the perimeter of the CDE.|Intrusion-detection and/or intrusion-prevention<br>techniques (such as IDS/IPS) compare the traffic<br>coming into the network with known “signatures”<br>and/or behaviors of thousands of compromise<br>types (hacker tools, Trojans, and other malware),<br>and then send alerts and/or stop the attempt as it|
|•<br>All traffic is monitored at critical points in the<br>CDE.|•<br>At critical points in the CDE.|happens. Without a proactive approach to detect<br>unauthorized activity, attacks on (or misuse of)|
|•<br>Personnel are alerted to suspected<br>compromises.<br>•<br>All intrusion-detection and prevention engines,<br>baselines, and signatures are kept up to date.|**11.5.1.b**Examine system configurations and<br>interview responsible personnel to verify intrusion-<br>detection and/or intrusion-prevention techniques<br>alert personnel of suspected compromises.|computer resources could go unnoticed for long<br>periods of time. The impact of an intrusion into the<br>CDE is, in many ways, a factor of the time that an<br>attacker has in the environment before being<br>detected.|
||**11.5.1.c**Examine system configurations and|**Good Practice**|
|**Customized Approach Objective**|vendor documentation to verify intrusion-detection<br>and/or intrusion-prevention techniques are<br>configured to keep all engines, baselines, and|Security alerts generated by these techniques<br>should be continually monitored, so that the<br>attempted or actual intrusions can be stopped,|
|Mechanisms to detect real-time suspicious or<br>anomalous network traffic that may be indicative of<br>threat actor activity are implemented. Alerts<br>generated by these mechanisms are responded to<br>by personnel, or by automated means that ensure<br>that system components cannot be compromised as<br>a result of the detected activity.|signatures up to date.|<br>and potential damage limited.<br>**Definitions**<br>Critical locations could include, but are not limited<br>to, network security controls between network<br>segments (for example, between a DMZ and an<br>internal network or between an in-scope and out-<br>of-scope network) and points protecting<br>connections between a less trusted and a more<br>trusted system component.|



Mechanisms to detect real-time suspicious or anomalous network traffic that may be indicative of threat actor activity are implemented. Alerts generated by these mechanisms are responded to by personnel, or by automated means that ensure that system components cannot be compromised as a result of the detected activity. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 283_ 



###### **Requirements and Testing Procedures** 

###### **Defined Approach Requirements** 

###### **Defined Approach Testing Procedures** 

**11.5.1.1** **_Additional requirement for service providers only:_** Intrusion-detection and/or intrusion-prevention techniques detect, alert on/prevent, and address covert malware communication channels. 

**11.5.1.1.a** **_Additional testing procedure for service provider assessments only:_** Examine documentation and configuration settings to verify that methods to detect and alert on/prevent covert malware communication channels are in place and operating. 

**11.5.1.1.b** **_Additional testing procedure for service provider assessments only:_** Examine the entity’s incident-response plan (Requirement 12.10.1) to verify it requires and defines a response in the event that covert malware communication channels are detected. 

**11.5.1.1.c** **_Additional testing procedure for service provider assessments only:_** Interview responsible personnel and observe processes to verify that personnel maintain knowledge of covert malware communication and control techniques and are knowledgeable about how to respond when malware is suspected. 

###### **Customized Approach Objective** 

Mechanisms are in place to detect and alert/prevent covert communications with command-and-control systems. Alerts generated by these mechanisms are responded to by personnel, or by automated means that ensure that such communications are blocked. 

###### **Guidance** 

###### **Purpose** 

Detecting covert malware communication attempts (for example, DNS tunneling) can help block the spread of malware laterally inside a network and the exfiltration of data. When deciding where to place this control, entities should consider critical locations in the network, and likely routes for covert channels. 

When malware establishes a foothold in an infected environment, it often tries to establish a communication channel to a command-andcontrol (C&C) server. Through the C&C server, the attacker communicates with and controls malware on compromised systems to deliver malicious payloads or instructions, or to initiate data exfiltration. In many cases, the malware will communicate with the C&C server indirectly via botnets, bypassing monitoring, blocking controls, and rendering these methods ineffective to detect the covert channels. 

_(continued on next page)_ 

_(continued on next page)_ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 284_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Applicability Notes**|**Good Practice**|
|This requirement applies only when the entity being<br>assessed is a service provider.|Methods that can help detect and address<br>malware communications channels include real-<br>time endpoint scanning, egress traffic filtering, an|
|_This requirement is a best practice until 31 March_|”allow” listing, data loss prevention tools, and|
|_2025, after which it will be required and must be_|network security monitoring tools such as|
|_fully considered during a PCI DSS assessment._|IDS/IPS. Additionally, DNS queries and<br>responses are a key data source used by network<br>defenders in support of incident response as well<br>as intrusion discovery. When these transactions<br>are collected for processing and analytics, they<br>can enable a number of valuable security analytic<br>scenarios.|
||It is important that organizations maintain up-to-<br>date knowledge of malware modes of operation,<br>as mitigating these can help detect and limit the<br>impact of malware in the environment.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 285_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**11.5.2**A change-detection mechanism (for example,<br>file integrity monitoring tools) is deployed as follows:<br>•<br>To alert personnel to unauthorized modification<br>(including changes, additions, and deletions) of<br>critical files.<br>•<br>To perform critical file comparisons at least<br>once weekly.|**11.5.2.a**Examine system settings, monitored files,<br>and results from monitoring activities to verify the<br>use of a change-detection mechanism.<br>**11.5.2.b**Examine settings for the change-detection<br>mechanism to verify it is configured in accordance<br>with all elements specified in this requirement.|Changes to critical system, configuration, or<br>content files can be an indicator an attacker has<br>accessed an organization’s system. Such<br>changes can allow an attacker to take additional<br>malicious actions, access cardholder data, and/or<br>conduct activities without detection or record.<br>A change detection mechanism will detect and<br>evaluate such changes to critical files and<br>generate alerts that can be responded to following|
|**Customized Approach Objective**||defined processes so that personnel can take<br>appropriate actions.|
|Critical files cannot be modified by unauthorized<br>personnel without an alert being generated.||_(continued on next page)_|
|_(continued on next page)_|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 286_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Applicability Notes**|If not implemented properly and the output of the<br>change-detection solution monitored, a malicious|
|For change-detection purposes, critical files are<br>usually those that do not regularly change, but the<br>modification of which could indicate a system<br>compromise or risk of compromise. Change-<br>detection mechanisms such as file integrity<br>monitoring products usually come pre-configured<br>with critical files for the related operating system.<br>Other critical files, such as those for custom<br>applications, must be evaluated and defined by the<br>entity (that is, the merchant or service provider).|individual could add, remove, or alter<br>configuration file contents, operating system<br>programs, or application executables.<br>Unauthorized changes, if undetected, could<br>render existing security controls ineffective and/or<br>result in cardholder data being stolen with no<br>perceptible impact to normal processing.<br>**Good Practice**<br>Examples of the types of files that should be<br>monitored include, but are not limited to:<br>•<br>System executables.<br>•<br>Application executables.<br>•<br>Configuration and parameter files.<br>•<br>Centrally stored, historical, or archived audit<br>logs.<br>•<br>Additional critical files determined by entity (for<br>example, through risk assessment or other<br>means).<br>**Examples**<br>Change-detection solutions such as file integrity<br>monitoring (FIM) tools check for changes,<br>additions, and deletions to critical files, and notify<br>when such changes are detected.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 287_ 



###### **Requirements and Testing Procedures Guidance** 

###### **11.6 Unauthorized changes on payment pages are detected and responded to.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**11.6.1**A change- and tamper-detection mechanism<br>is deployed as follows:<br>•<br>To alert personnel to unauthorized modification<br>(including indicators of compromise, changes,|**11.6.1.a**Examine system settings, monitored<br>payment pages, and results from monitoring<br>activities to verify the use of a change- and tamper-<br>detection mechanism.|Many web pages now rely on assembling objects,<br>including active content (primarily JavaScript),<br>from multiple internet locations. Additionally, the<br>content of many web pages is defined using<br>content management and tag management|
|additions, and deletions) to the security-<br>impacting HTTP headers and the script contents<br>of payment pages as received by the consumer<br>browser.|**11.6.1.b**Examine configuration settings to verify<br>the mechanism is configured in accordance with all<br>elements specified in this requirement.|systems that may not be possible to monitor using<br>traditional change detection mechanisms.<br>Therefore, the only place to detect changes or<br>indicators of malicious activity is in the consumer|
|•<br>The mechanism is configured to evaluate the<br>received HTTP headers and payment pages.|**11.6.1.c**If the mechanism functions are performed<br>at an entity-defined frequency examine the entity’s|browser as the page is constructed and all<br>JavaScript interpreted.|
|•<br>The mechanism functions are performed as<br>follows:<br>– At least weekly<br>**OR**|,<br>targeted risk analysis for determining the frequency<br>to verify the risk analysis was performed in<br>accordance with all elements specified at<br>Requirement 12.3.1.|By comparing the current version of the HTTP<br>header and the active content of payment pages<br>as received by the consumer browser with prior or<br>known versions, it is possible to detect<br>unauthorized changes that may indicate a|
|– Periodically (at the frequency defined in the<br>entity’s targeted risk analysis, which is<br>performed according to all elements<br>specified in Requirement 12.3.1).|**11.6.1.d**Examine configuration settings and<br>interview personnel to verify the mechanism<br>functions are performed either:<br>•<br>At least weekly|skimming attack, or an attempt to disable a<br>control designed to protect against, or to detect,<br>skimming attacks.<br>Additionally, by looking for known indicators of<br>|
|||compromise and script elements or behavior|
|**Customized Approach Objective**|**OR**<br>•<br>At the frequency defined in the entity’s targeted|<br>typical of skimmers, suspicious alerts can be<br>raised.|
|E-commerce skimming code or techniques cannot<br>be added to payment pages as received by the<br>consumer browser without a timely alert being<br>generated. Anti-skimming measures cannot be<br>removed from payment pages without a prompt alert<br>being generated.|risk analysis performed for this requirement.|_(continued on next page)_|
|_(continued on next page)_|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 288_ 



###### **Requirements and Testing Procedures Guidance** 

###### **Applicability Notes** 

This requirement also applies to entities with a webpage(s) that includes a TPSP’s/payment processor’s embedded payment page/form (for example, one or more inline frames or iframes.) 

This requirement does not apply to an entity for scripts in a TPSP’s/payment processor’s embedded payment page/form (for example, one or more iframes), where the entity includes a TPSP’s/payment processor’s payment page/form on its webpage. Scripts in the TPSP’s/payment processor’s embedded payment page/form are the responsibility of the TPSP/payment processor to manage in accordance with this requirement. 

The intention of this requirement is not that an entity installs software in the systems or browsers of its consumers, but rather that the entity uses techniques such as those described under Examples in the Guidance column to prevent and detect unexpected script activities. 

_This requirement is a best practice until 31 March 2025, after which it will be required and must be fully considered during a PCI DSS assessment._ 

- **Good Practice** Where an entity includes a TPSP’s/payment processor’s embedded payment page/form on its webpage, the entity should expect the TPSP/payment processor to provide evidence that the TPSP/payment processor is meeting this requirement, in accordance with the TPSP’s/payment processor’s PCI DSS assessment and Requirement 12.9. **Examples** Mechanisms that detect and report on changes to the headers and content of the payment page could include, but are not limited to, a combination of the following techniques: • Violations of the Content Security Policy (CSP) can be reported to the entity using the _report-to_ or _report-uri_ CSP directives. 

- • Changes to the CSP itself can indicate tampering. 

- • External monitoring by systems that request and analyze the received web pages (also known as synthetic user monitoring) can detect changes to JavaScript in payment pages and alert personnel. 

- • Embedding tamper-resistant, tamper-detection script in the payment page can alert and block when malicious script behavior is detected. 

- • Reverse proxies and Content Delivery Networks can detect changes in scripts and alert personnel. 

- The above list of mechanisms is not exhaustive, and the use of any one mechanism is not necessarily a full detection and reporting mechanism. Often, these mechanisms are subscription or cloudbased, but can also be based on custom and bespoke solutions. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 289_ 



### **Maintain an Information Security Policy** 

#### **_Requirement 12: Support Information Security with Organizational Policies and Programs_** 

**Sections** 

- **12.1** A comprehensive information security policy that governs and provides direction for protection of the entity’s information assets is known and current. 

- **12.2** Acceptable use policies for end-user technologies are defined and implemented. 

- **12.3** Risks to the cardholder data environment are formally identified, evaluated, and managed. 

- **12.4** PCI DSS compliance is managed. 

- **12.5** PCI DSS scope is documented and validated. 

- **12.6** Security awareness education is an ongoing activity. 

- **12.7** Personnel are screened to reduce risks from insider threats. 

- **12.8** Risk to information assets associated with third-party service provider (TPSP) relationships is managed. 

- **12.9** Third-party service providers (TPSPs) support their customers’ PCI DSS compliance. 

- **12.10** Suspected and confirmed security incidents that could impact the CDE are responded to immediately. 

###### **Overview** 

The organization’s overall information security policy sets the tone for the whole entity and informs personnel what is expected of them. All personnel should be aware of the sensitivity of cardholder data and their responsibilities for protecting it. 

For the purposes of Requirement 12, “personnel” refers to full-time and part-time employees, temporary employees, contractors, and consultants with security responsibilities for protecting account data or that can impact the security of cardholder data and/or sensitive authentication data. 

Refer to _Appendix G_ for definitions of PCI DSS terms. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 290_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

**12.1 A comprehensive information security policy that governs and provides direction for protection of the entity’s information assets is known and current.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.1.1**An overall information security policy is:<br>•<br>Established.<br>•<br>Published.<br>•<br>Maintained.<br>•<br>Disseminated to all relevant personnel, as well<br>as to relevant vendors and business partners.|**12.1.1**Examine the information security policy and<br>interview personnel to verify that the overall<br>information security policy is managed in<br>accordance with all elements specified in this<br>requirement.|An organization’s overall information security<br>policy ties to and governs all other policies and<br>procedures that define protection of cardholder<br>data.<br>The information security policy communicates<br>management’s intent and objectives regarding the<br>protection of its most valuable assets, including<br>cardholder data.|
|**Customized Approach Objective**||Without an information security policy, individuals<br>will make their own value decisions on the|
|The strategic objectives and principles of<br>information security are defined, adopted, and<br>known to all personnel.||controls that are required within the organization<br>which may result in the organization neither<br>meeting its legal, regulatory, and contractual<br>obligations, nor being able to adequately protect<br>its assets in a consistent manner.<br>To ensure the policy is implemented, it is<br>important that all relevant personnel within the<br>organization, as well as relevant third parties,<br>vendors, and business partners are aware of the<br>organization’s information security policy and their<br>responsibilities for protecting information assets.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 291_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**12.1.1**_(continued)_|**Good Practice**<br>The security policy for the organization identifies<br>the purpose, scope, accountability, and<br>information that clearly defines the organization’s<br>position regarding information security.<br>The overall information security policy differs from<br>individual security policies that address specific<br>technology or security disciplines. This policy sets<br>forth the directives for the entire organization<br>whereas individual security policies align and<br>support the overall security policy and<br>communicate specific objectives for technology or<br>security disciplines.<br>It is important that all relevant personnel within<br>the organization, as well as relevant third parties,<br>vendors, and business partners are aware of the<br>organization’s information security policy and their<br>responsibilities for protecting information assets.<br>**Definitions**|
||“Relevant” for this requirement means that the<br>information security policy is disseminated to<br>those with roles applicable to some or all the<br>topics in the policy, either within the company or<br>because of services/functions performed by a<br>vendor or third party.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 292_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**12.1.2**The information security policy is:<br>•<br>Reviewed at least once every 12 months.<br>•<br>Updated as needed to reflect changes to<br>business objectives or risks to the environment.|**12.1.2**Examine the information security policy and<br>interview responsible personnel to verify the policy<br>is managed in accordance with all elements<br>specified in this requirement.|Security threats and associated protection<br>methods evolve rapidly. Without updating the<br>information security policy to reflect relevant<br>changes, new measures to defend against these<br>threats may not be addressed.|
|**Customized Approach Objective**|||
|The information security policy continues to reflect<br>the organization’s strategic objectives and<br>principles.|||
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**12.1.3**The security policy clearly defines<br>information security roles and responsibilities for all<br>personnel, and all personnel are aware of and<br>acknowledge their information security<br>responsibilities.|**12.1.3.a**Examine the information security policy to<br>verify that they clearly define information security<br>roles and responsibilities for all personnel.<br>**12.1.3.b**Interview personnel in various roles to<br>verify they understand their information security<br>responsibilities.|Without clearly defined security roles and<br>responsibilities assigned, there could be misuse<br>of the organization’s information assets or<br>inconsistent interaction with information security<br>personnel, leading to insecure implementation of<br>technologies or use of outdated or insecure<br>technologies.|
|**Customized Approach Objective**|**12.1.3.c**Examine documented evidence to verify<br>personnel acknowledge their information security<br>responsibilities.||
|Personnel understand their role in protecting the<br>entity’s cardholder data.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 293_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.1.4**Responsibility for information security is<br>formally assigned to a Chief Information Security<br>Officer or other information security knowledgeable<br>member of executive management. .<br>**Customized Approach Objective**|**12.1.4**Examine the information security policy to<br>verify that information security is formally assigned<br>to a Chief Information Security Officer or other<br>information security-knowledgeable member of<br>executive management.|To ensure someone with sufficient authority and<br>responsibility is actively managing and<br>championing the organization’s information<br>security program, accountability and responsibility<br>for information security needs to be assigned at<br>the executive level within an organization.<br>**Good Practice**|
|A designated member of executive management is<br>responsible for information security.||These executive management positions are often<br>at the most senior level of management and are<br>part of the chief executive level or C-level,<br>typically reporting to the Chief Executive Officer or<br>the Board of Directors. Information security<br>knowledge for this executive management role<br>can be indicated by work experience, education,<br>and/or relevant professional certifications. The<br>expectation is that this individual can provide<br>assurance about the implementation of an<br>effective security program and ensure the right<br>technical experts are employed.<br>Entities should also consider transition and/or<br>succession plans for these key personnel to avoid<br>potential gaps in critical security activities.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 294_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **12.2 Acceptable use policies for end-user technologies are defined and implemented.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.2.1**Acceptable use policies for end-user<br>technologies are documented and implemented,<br>including:<br>•<br>Explicit approval by authorized parties.<br>•<br>Acceptable uses of the technology.<br>•<br>List of products approved by the company for<br>employee use, including hardware and software.|**12.2.1**Examine the acceptable use policies for<br>end-user technologies and interview responsible<br>personnel to verify processes are documented and<br>implemented in accordance with all elements<br>specified in this requirement.|End-user technologies are a significant<br>investment and may pose significant risk to an<br>organization if not managed properly. Acceptable<br>use policies outline the expected behavior from<br>personnel when using the organization’s<br>information technology and reflect the<br>organization’s risk tolerance<br>These policies instruct personnel on what they<br>can and cannot do with company equipment and|
|**Customized Approach Objective**||instruct personnel on correct and incorrect uses of<br>company Internet and email resources. Such|
|The use of end-user technologies is defined and<br>managed to ensure authorized usage.||policies can legally protect an organization and<br>allow it to act when the policies are violated.<br>**Good Practice**|
|**Applicability Notes**||It is important that usage policies are supported|
|Examples of end-user technologies for which<br>acceptable use policies are expected include, but<br>are not limited to, remote access and wireless<br>technologies, laptops, tablets, mobile phones, and<br>removable electronic media, email usage, and<br>Internet usage.||by technical controls to manage the enforcement<br>of the policies.<br>Structuring polices as simple “do” and “do not”<br>requirements that are linked to a purpose can<br>help remove ambiguity and provide personnel<br>with the context for the requirement.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 295_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **12.3 Risks to the cardholder data environment are formally identified, evaluated, and managed.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.3.1**For each PCI DSS requirement that specifies<br>completion of a targeted risk analysis, the analysis<br>is documented and includes:<br>•<br>Identification of the assets being protected.<br>•<br>Identification of the threat(s) that the<br>requirement is protecting against.<br>•<br>Identification of factors that contribute to the<br>likelihood and/or impact of a threat being<br>realized.|**12.3.1**Examine documented policies and<br>procedures to verify a process is defined for<br>performing targeted risk analyses for each PCI<br>DSS requirement that specifies completion of a<br>targeted risk analysis, and that the process<br>includes all elements specified in this requirement.|Some PCI DSS requirements allow an entity to<br>define how frequently an activity is performed<br>based on the risk to the entity’s environment.<br>Performing this risk analysis according to a<br>methodology ensures validity and consistency<br>with policies and procedures.<br>This targeted risk analysis (as opposed to a<br>traditional enterprise-wide risk assessment)<br>focuses on those PCI DSS requirements that<br>allow an entity flexibility about how frequently an<br>|
|•<br>Resulting analysis that determines, and includes<br>justification for, how the frequency or processes<br>defined by the entity to meet the requirement<br>minimize the likelihood and/or impact of the<br>threat being realized.<br>•<br>Review of each targeted risk analysis at least<br>once every 12 months to determine whether the<br>results are still valid or if an updated risk<br>analysis is needed.<br>•<br>Performance of updated risk analyses when<br>needed, as determined by the annual review.||entity performs a given control. For this risk<br>analysis, the entity carefully evaluates each PCI<br>DSS requirement that provides this flexibility and<br>determines the frequency that supports adequate<br>security for the entity, and the level of risk the<br>entity is willing to accept.<br>The risk analysis identifies the specific assets,<br>such as the system components and data—for<br>example, log files, or credentials—that the<br>requirement is intended to protect, as well as the<br>threat(s) or outcomes that the requirement is<br>protecting the assets from—for example,|
|**Customized Approach Objective**||malware, an undetected intruder, or misuse of<br>credentials. Examples of factors that could|
|Up to date knowledge and assessment of risks to<br>the CDE are maintained.||contribute to likelihood or impact include any that<br>could increase the vulnerability of an asset to a<br>threat—for example, exposure to untrusted|
|**Applicability Notes**<br>_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._||networks, complexity of environment, or high staff<br>turnover—as well as the criticality of the system<br>components, or volume and sensitivity of the<br>data, being protected.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 296_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**12.3.1**_(continued)_|Reviewing the results of these targeted risk<br>analyses at least once every 12 months and upon<br>changes that could impact the risk to the<br>environment allows the organization to ensure the<br>risk analysis results remain current with<br>organizational changes and evolving threats,<br>trends, and technologies, and that the selected<br>frequencies still adequately address the entity’s<br>risk.|
||**Good Practice**<br>An enterprise-wide risk assessment, which is a<br>point-in-time activity that enables entities to<br>identify threats and associated vulnerabilities, is<br>recommended, but is not required, for entities to<br>determine and understand broader and emerging<br>threats with the potential to negatively impact its<br>business. This enterprise-wide risk assessment<br>could be established as part of an overarching<br>risk management program that is used as an<br>input to the annual review of an organization's<br>overall information security policy (see<br>Requirement 12.1.1).<br>Examples of risk-assessment methodologies for<br>enterprise-wide risk assessments include, but are<br>not limited to, ISO_27005_and NIST_SP 800-30_.<br>**Further Information**<br>Refer to the following documents on the PCI SSC<br>website:<br>•<br>_Information Supplement: TRA Guidance_|
||•<br>_Sample Template: TRA for Activity Frequency_.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 297_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.3.2**A targeted risk analysis is performed for each<br>PCI DSS requirement that the entity meets with the<br>customized approach, to include:<br>•<br>Documented evidence detailing each element<br>specified in Appendix D: Customized Approach<br>(including, at a minimum, a controls matrix and<br>risk analysis).<br>•<br>Approval of documented evidence by senior<br>management.|**12.3.2**Examine the documented targeted risk-<br>analysis for each PCI DSS requirement that the<br>entity meets with the customized approach to verify<br>that documentation for each requirement exists<br>and is in accordance with all elements specified in<br>this requirement.|A risk analysis following a repeatable and robust<br>methodology enables an entity to meet the<br>customized approach objective.<br>**Definitions**<br>The customized approach to meeting a PCI DSS<br>requirement allows entities to define the controls<br>used to meet a given requirement’s stated<br>Customized Approach Objective in a way that<br>does not strictly follow the defined requirement.<br>These controls are expected to at least meet or|
|•<br>Performance of the targeted analysis of risk at<br>least once every 12 months.||exceed the security provided by the defined<br>requirement and require extensive documentation|
|**Customized Approach Objective**||by the entity using the customized approach.<br>**Further Information**|
|This requirement is part of the customized approach<br>and must be met for those using the customized<br>approach.||See_Appendix D: Customized Approach_for<br>instructions on how to document the required<br>evidence for the customized approach.<br>See_PCI DSS v4.x: Sample Templates to Support_|
|**Applicability Notes**||_Customized Approach_on the PCI SSC website<br>for templates that entities may use to document|
|This requirement only applies to entities using a<br>Customized Approach.||their customized controls. Note that while use of<br>the templates is optional, the information specified<br>within each template must be documented and<br>provided to each entity’s assessor.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 298_ 



###### **Requirements and Testing Procedures** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|
|---|---|
|**12.3.3**Cryptographic cipher suites and protocols in|**12.3.3**Examine documentation for cryptographic|
|use are documented and reviewed at least once|suites and protocols in use and interview personnel|
|every 12 months, including at least the following:|to verify the documentation and review is in|
|•<br>An up-to-date inventory of all cryptographic|accordance with all elements specified in this<br>|
|cipher suites and protocols in use including|requirement.|



- An up-to-date inventory of all cryptographic cipher suites and protocols in use, including purpose and where used. 

- Active monitoring of industry trends regarding continued viability of all cryptographic cipher suites and protocols in use. 

- Documentation of a plan, to respond to anticipated changes in cryptographic vulnerabilities. 

###### **Customized Approach Objective** 

The entity is able to respond quickly to any vulnerabilities in cryptographic protocols or algorithms, where those vulnerabilities affect protection of cardholder data. 

###### **Applicability Notes** 

The requirement applies to all cryptographic cipher suites and protocols used to meet PCI DSS requirements, including, but not limited to, those used to render PAN unreadable in storage and transmission, to protect passwords, and as part of authenticating access. _This requirement is a best practice until 31 March 2025, after which it will be required and must be fully considered during a PCI DSS assessment._ 

###### **Guidance** 

###### **Purpose** 

Protocols and encryption strengths may quickly change or be deprecated due to identification of vulnerabilities or design flaws. In order to support current and future data security needs, entities need to know where cryptography is used and understand how they would be able to respond rapidly to changes impacting the strength of their cryptographic implementations. **Good Practice** Cryptographic agility is important to ensure an alternative to the original encryption method or cryptographic primitive is available, with plans to upgrade to the alternative without significant change to system infrastructure. For example, if the entity is aware of when protocols or algorithms will be deprecated by standards bodies, proactive plans will help the entity to upgrade before the deprecation is impactful to operations. **Definitions** “Cryptographic agility” refers to the ability to monitor and manage the encryption and related verification technologies deployed across an organization. 

###### **Further Information** 

Refer to _NIST SP 800-131a, Transitioning the Use of Cryptographic Algorithms and Key Lengths_ . 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 299_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.3.4**Hardware and software technologies in use<br>are reviewed at least once every 12 months,<br>including at least the following:<br>•<br>Analysis that the technologies continue to<br>receive security fixes from vendors promptly.<br>•<br>Analysis that the technologies continue to<br>support (and do not preclude) the entity’s PCI|**12.3.4**Examine documentation for the review of<br>hardware and software technologies in use and<br>interview personnel to verify that the review is in<br>accordance with all elements specified in this<br>requirement.|Hardware and software technologies are<br>constantly evolving, and organizations need to be<br>aware of changes to the technologies they use,<br>as well as the evolving threats to those<br>technologies to ensure that they can prepare for,<br>and manage, vulnerabilities in hardware and<br>software that will not be remediated by the vendor<br>or developer.**Good Practice**|
|DSS compliance.||Organizations should review firmware versions to|
|•<br>Documentation of any industry announcements<br>or trends related to a technology, such as when<br>a vendor has announced “end of life” plans for a<br>technology.<br>•<br>Documentation of a plan, approved by senior<br>management, to remediate outdated<br>technologies, including those for which vendors<br>have announced “end of life” plans.||ensure they remain current and supported by the<br>vendors. Organizations also need to be aware of<br>changes made by technology vendors to their<br>products or processes to understand how such<br>changes may impact the organization’s use of the<br>technology.<br>Regular reviews of technologies that impact or<br>influence PCI DSS controls can assist with<br>purchasing, usage, and deployment strategies,|
|**Customized Approach Objective**||and ensure controls that rely on those<br>technologies remain effective. These reviews|
|The entity’s hardware and software technologies are<br>up to date and supported by the vendor. Plans to<br>remove or replace all unsupported system<br>components are reviewed periodically.||include, but are not limited to, reviewing<br>technologies that are no longer supported by the<br>vendor and/or no longer meet the security needs<br>of the organization.|
|**Applicability Notes**|||
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_|||
|_fully considered during a PCI DSS assessment._|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 300_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

**12.4 PCI DSS compliance is managed. Defined Approach Requirements Defined Approach Testing Procedures Purpose** Executive management assignment of PCI DSS **12.4.1** **_Additional requirement for service_ 12.4.1** **_Additional testing procedure for service_** compliance responsibilities ensures executive- **_providers only:_** Responsibility is established by **_provider assessments only:_** Examine level visibility into the PCI DSS compliance executive management for the protection of documentation to verify that executive program and allows for the opportunity to ask cardholder data and a PCI DSS compliance management has established responsibility for the appropriate questions to determine the program to include: protection of cardholder data and a PCI DSS effectiveness of the program and influence • Overall accountability for maintaining PCI DSS compliance program in accordance with all strategic priorities. compliance. elements specified in this requirement. • Defining a charter for a PCI DSS compliance program and communication to executive management. **Customized Approach Objective** Executives are responsible and accountable for security of cardholder data. **Applicability Notes** This requirement applies only when the entity being assessed is a service provider. Executive management may include C-level positions, board of directors, or equivalent. The specific titles will depend on the particular organizational structure. Responsibility for the PCI DSS compliance program may be assigned to individual roles and/or to business units within the organization. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 301_ 



###### **Requirements and Testing Procedures** 

**Defined Approach Requirements Defined Approach Testing Procedures 12.4.2** **_Additional requirement for service_ 12.4.2.a** **_Additional testing procedure for providers only:_** Reviews are performed at least **_service provider assessments only:_** Examine once every three months to confirm that personnel policies and procedures to verify that processes are performing their tasks in accordance with all are defined for conducting reviews to confirm that security policies and operational procedures. personnel are performing their tasks in accordance Reviews are performed by personnel other than with all security policies and all operational those responsible for performing the given task and procedures, including but not limited to the tasks include, but are not limited to, the following tasks: specified in this requirement. 

- Daily log reviews. 

**12.4.2.b** **_Additional testing procedure for service provider assessments only:_** Interview responsible personnel and examine records of reviews to verify that reviews are performed: 

- Configuration reviews for network security controls. 

- Applying configuration standards to new systems. 

   - At least once every three months. 

- Responding to security alerts. 

   - By personnel other than those responsible for performing the given task. 

- Change-management processes. 

###### **Customized Approach Objective** 

The operational effectiveness of critical PCI DSS controls is verified periodically by manual inspection of records. 

**Applicability Notes** This requirement applies only when the entity being assessed is a service provider. 

###### **Guidance** 

###### **Purpose** 

Regularly confirming that security policies and procedures are being followed provides assurance that the expected controls are active and working as intended. This requirement is distinct from other requirements that specify a task to be performed. The objective of these reviews is not to reperform other PCI DSS requirements, but to confirm that security activities are being performed on an ongoing basis. 

###### **Good Practice** 

These reviews can also be used to verify that appropriate evidence is being maintained—for example, audit logs, vulnerability scan reports, reviews of network security control rulesets—to assist in the entity’s preparation for its next PCI DSS assessment. 

###### **Examples** 

Looking at Requirement 1.2.7 as one example, Requirement 12.4.2 is met by confirming, at least once every three months, that reviews of configurations of network security controls have occurred at the required frequency. On the other hand, Requirement 1.2.7 is met by reviewing those configurations as specified in the requirement. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 302_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

**Defined Approach Requirements Defined Approach Testing Procedures Purpose** The intent of these independent checks is to **12.4.2.1** **_Additional requirement for service_ 12.4.2.1** **_Additional testing procedure for_** confirm whether security activities are being **_providers only:_** Reviews conducted in accordance **_service provider assessments only:_** Examine performed on an ongoing basis. These reviews with Requirement 12.4.2 are documented to include: documentation from the reviews conducted in can also be used to verify that appropriate • Results of the reviews. accordance with PCI DSS Requirement 12.4.2 to evidence is being maintained—for example, audit verify the documentation includes all elements • Documented remediation actions taken for any logs, vulnerability scan reports, reviews of specified in this requirement. tasks that were found to not be performed at network security control rulesets—to assist in the Requirement 12.4.2. entity’s preparation for its next PCI DSS assessment. • Review and sign-off of results by personnel assigned responsibility for the PCI DSS compliance program. 

**Customized Approach Objective** Findings from operational effectiveness reviews are evaluated by management; appropriate remediation activities are implemented. **Applicability Notes** This requirement applies only when the entity being assessed is a service provider. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 303_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **12.5 PCI DSS scope is documented and validated.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.5.1**An inventory of system components that are<br>in scope for PCI DSS, including a description of<br>function/use, is maintained and kept current.|**12.5.1.a**Examine the inventory to verify it includes<br>all in-scope system components and a description<br>of function/use for each.|Maintaining a current list of all system<br>components will enable an organization to define<br>the scope of its environment and implement PCI<br>DSS requirements accurately and efficiently.|
|**Customized Approach Objective**|**12.5.1.b**Interview personnel to verify the inventory<br>is kept current.|Without an inventory, some system components<br>could be overlooked and be inadvertently<br>excluded from the organization’s configuration<br>standards.|
|All system components in scope for PCI DSS are<br>identified and known.||**Good Practice**<br>If an entity keeps an inventory of all assets, those<br>system components in scope for PCI DSS should<br>be clearly identifiable among the other assets.<br>Inventories should include containers or images<br>that may be instantiated.<br>Assigning an owner to the inventory helps to<br>ensure the inventory stays current.<br>**Examples**<br>Methods to maintain an inventory include as a<br>database, as a series of files, or in an inventory-<br>management tool.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 304_ 



|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**12.5.2**PCI DSS scope is documented and<br>confirmed by the entity at least once every 12<br>months and upon significant change to the in-scope<br>environment. At a minimum, the scoping validation<br>includes:<br>•<br>Identifying all data flows for the various payment<br>stages (for example, authorization, capture|**12.5.2.a**Examine documented results of scope<br>reviews and interview personnel to verify that the<br>reviews are performed:<br>•<br>At least once every 12 months.<br>•<br>After significant changes to the in-scope<br>environment.|Frequent validation of PCI DSS scope helps to<br>ensure PCI DSS scope remains up to date and<br>aligned with changing business objectives, and<br>therefore that security controls are protecting all<br>appropriate system components.<br>**Good Practice**<br>Accurate scoping involves critically evaluating the<br>|
|settlement, chargebacks, and refunds) and<br>acceptance channels (for example, card-<br>present, card-not-present, and e-commerce).<br>•<br>Updating all data-flow diagrams per<br>Requirement 1.2.4.<br>•<br>Identifying all locations where account data is<br>stored, processed, and transmitted, including but<br>not limited to: 1) any locations outside of the<br>currently defined CDE, 2) applications that<br>process CHD, 3) transmissions between<br>systems and networks, and 4) file backups.|**12.5.2.b**Examine documented results of scope<br>reviews performed by the entity to verify that PCI<br>DSS scoping confirmation activity includes all<br>elements specified in this requirement.|CDE and all connected system components to<br>determine the necessary coverage for PCI DSS<br>requirements. Scoping activities, including careful<br>analysis and ongoing monitoring, help to ensure<br>that in-scope systems are appropriately secured.<br>When documenting account data locations, the<br>entity can consider creating a table or<br>spreadsheet that includes the following<br>information:<br>•<br>Data stores (databases, files, cloud, etc.),<br>including the purpose of data storage and the<br>retention period,|
|•<br>Identifying all system components in the CDE,<br>connected to the CDE, or that could impact<br>security of the CDE.||•<br>Which CHD elements are stored (PAN, expiry<br>date, cardholder name, and/or any elements<br>of SAD prior to completion of authorization),|
|•<br>Identifying all segmentation controls in use and<br>the environment(s) from which the CDE is<br>segmented, including justification for<br>environments being out of scope.<br>•<br>Identifying all connections from third-party<br>entities with access to the CDE.||•<br>How data is secured (type of encryption and<br>strength, hashing algorithm and strength,<br>truncation, tokenization),<br>•<br>How access to data stores is logged,<br>including a description of logging<br>mechanism(s) in use (enterprise solution,|
|•<br>Confirming that all identified data flows, account<br>data, system components, segmentation<br>controls, and connections from third parties with<br>||<br>application level, operating system level,<br>etc.).<br>_(continued on next page)_|



- Identifying all connections from third-party entities with access to the CDE. 

- • Confirming that all identified data flows, account data, system components, segmentation controls, and connections from third parties with access to the CDE are included in scope. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 305_ 



###### **Requirements and Testing Procedures Guidance** 

|**Customized Approach Objective**<br>PCI DSS scope is verified periodically, and after<br>significant changes, by comprehensive analysis and<br>appropriate technical measures.<br>**Applicability Notes**|In addition to internal systems and networks, all<br>connections from third-party entities—for<br>example, business partners, entities providing<br>remote support services, and other service<br>providers—need to be identified to determine<br>inclusion for PCI DSS scope. Once the in-scope<br>connections have been identified, the applicable<br>PCI DSS controls can be implemented to reduce|
|---|---|
|This annual confirmation of PCI DSS scope is an<br>activity expected to be performed by the entity<br>under assessment, and is not the same, nor is it<br>intended to be replaced by, the scoping confirmation<br>performed by the entity’s assessor during the<br>annual assessment.|the risk of a third-party connection being used to<br>compromise an entity’s CDE.<br>A data discovery tool or methodology can be used<br>to facilitate identifying all sources and locations of<br>PAN, and to look for PAN that resides on systems<br>and networks outside the currently defined CDE<br>or in unexpected places within the defined CDE—<br>for example, in an error log or memory dump file.<br>This approach can help ensure that previously<br>unknown locations of PAN are detected and that<br>the PAN is either eliminated or properly secured.<br>**Further Information**|
||For additional guidance, refer to_Information_<br>_Supplement: Guidance for PCI DSS Scoping and_<br>_Network Segmentation_.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 306_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.5.2.1** **_Additional requirement for service_**<br>**_providers only:_**PCI DSS scope is documented and<br>confirmed by the entity at least once every six<br>months and upon significant change to the in-scope<br>environment. At a minimum, the scoping validation<br>includes all the elements specified in Requirement<br>12.5.2.|**12.5.2.1.a** **_Additional testing procedure for_**<br>**_service provider assessments only:_**Examine<br>documented results of scope reviews and interview<br>personnel to verify that reviews per Requirement<br>12.5.2 are performed:<br>•<br>At least once every six months, and<br>•<br>After significant changes|Service providers typically have access to greater<br>volumes of cardholder data than do merchants, or<br>can provide an entry point that can be exploited to<br>then compromise multiple other entities. Service<br>providers also typically have larger and more<br>complex networks that are subject to more<br>frequent change. The probability of overlooked<br>changes to scope in complex and dynamic<br>networks is greater in service-providers|
||**12.5.2.1.b** **_Additional testing procedure for_**<br>**_service provider assessments only:_**Examine|environments.<br>Validating PCI DSS scope more frequently is|
|**Customized Approach Objective**<br>The accuracy of PCI DSS scope is verified to be<br>continuously accurate by comprehensive analysis<br>and appropriate technical measures.|documented results of scope reviews to verify that<br>scoping validation includes all elements specified<br>in Requirement 12.5.2.|likely to discover such overlooked changes before<br>they can be exploited by an attacker.|
|**Applicability Notes**|||
|This requirement applies only when the entity being<br>assessed is a service provider.|||
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 307_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.5.3** **_Additional requirement for service_**<br>**_providers only:_** Significant changes to<br>organizational structure result in a documented<br>(internal) review of the impact to PCI DSS scope<br>and applicability of controls, with results<br>communicated to executive management.|**12.5.3.a** **_Additional testing procedure for_**<br>**_service provider assessments only:_**Examine<br>policies and procedures to verify that processes<br>are defined such that a significant change to<br>organizational structure results in documented<br>review of the impact to PCI DSS scope and<br>applicability of controls.|An organization’s structure and management<br>define the requirements and protocol for effective<br>and secure operations. Changes to this structure<br>could have negative effects to existing controls<br>and frameworks by reallocating or removing<br>resources that once supported PCI DSS controls<br>or inheriting new responsibilities that may not<br>have established controls in place. Therefore, it is|
||**12.5.3.b** **_Additional testing procedure for_**<br>|important to revisit PCI DSS scope and controls<br>when there are changes to an organization’s|
|**Customized Approach Objective**<br>PCI DSS scope is confirmed after significant<br>organizational change.|**_service provider assessments only:_**Examine<br>documentation (for example, meeting minutes) and<br>interview responsible personnel to verify that<br>significant changes to organizational structure<br>resulted in documented reviews that included all<br>elements specified in this requirement, with results|structure and management to ensure controls are<br>in place and active.<br>**Examples**<br>Changes to organizational structure include, but<br>are not limited to, company mergers or|
|**Applicability Notes**|communicated to executive management.|acquisitions, and significant changes or<br>reassignments of personnel with responsibility for|
|This requirement applies only when the entity being<br>assessed is a service provider.||security controls.|
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 308_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **12.6 Security awareness education is an ongoing activity.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.6.1**A formal security awareness program is<br>implemented to make all personnel aware of the<br>entity’s information security policy and procedures,<br>and their role in protecting the cardholder data.<br>**Customized Approach Objective**|**12.6.1**Examine the security awareness program to<br>verify it provides awareness to all personnel about<br>the entity’s information security policy and<br>procedures, and personnel’s role in protecting the<br>cardholder data.|If personnel are not educated about their<br>company’s information security policies and<br>procedures and their own security responsibilities,<br>security safeguards and processes that have<br>been implemented may become ineffective<br>through unintentional errors or intentional actions.|
|Personnel are knowledgeable about the threat<br>landscape, their responsibility for the operation of<br>relevant security controls, and are able to access<br>assistance and guidance when required.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 309_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.6.2**The security awareness program is:<br>•<br>Reviewed at least once every 12 months, and<br>•<br>Updated as needed to address any new threats<br>and vulnerabilities that may impact the security<br>of the entity’s cardholder data and/or sensitive<br>authentication data, or the information provided<br>to personnel about their role in protecting<br>cardholder data.|**12.6.2**Examine security awareness program<br>content, evidence of reviews, and interview<br>personnel to verify that the security awareness<br>program is in accordance with all elements<br>specified in this requirement.|The threat environment and an entity’s defenses<br>are not static. As such, the security awareness<br>program materials must be updated as frequently<br>as needed to ensure that the education received<br>by personnel is up to date and represents the<br>current threat environment.|
|**Customized Approach Objective**|||
|The content of security awareness material is<br>reviewed and updated periodically.|||
|**Applicability Notes**|||
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 310_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.6.3**Personnel receive security awareness<br>training as follows:<br>•<br>Upon hire and at least once every 12 months.<br>•<br>Multiple methods of communication are used.<br>•<br>Personnel acknowledge at least once every 12<br>months that they have read and understood the<br>information security policy and procedures.|**12.6.3.a**Examine security awareness program<br>records to verify that personnel attend security<br>awareness training upon hire and at least once<br>every 12 months.<br>**12.6.3.b**Examine security awareness program<br>materials to verify the program includes multiple<br>methods of communicating awareness and<br>educating personnel.|Training of personnel ensures they receive the<br>information about the importance of information<br>security and that they understand their role in<br>protecting the organization.<br>Requiring an acknowledgment by personnel helps<br>ensure that they have read and understood the<br>security policies and procedures, and that they<br>have made and will continue to make a<br>commitment to comply with these policies.<br>**Good Practice**|
||**12.6.3.c**Interview personnel to verify they have<br>completed awareness training and are aware of<br>their role in protecting cardholder data.|Entities may incorporate new-hire training as part<br>of the Human Resources onboarding process.<br>Training should outline the security-related “dos”<br>and “don’ts.” Periodic refresher training reinforces|
||**12.6.3.d**Examine security awareness program<br>materials and personnel acknowledgments to|key security processes and procedures that may<br>be forgotten or bypassed.|
|**Customized Approach Objective**<br>Personnel remain knowledgeable about the threat<br>landscape, their responsibility for the operation of<br>relevant security controls, and are able to access<br>assistance and guidance when required.|verify that personnel acknowledge at least once<br>every 12 months that they have read and<br>understand the information security policy and<br>procedures.|Entities should consider requiring security<br>awareness training anytime personnel transfer<br>into roles where they can impact the security of<br>cardholder data and/or sensitive authentication<br>data from roles where they did not have this<br>impact.<br>Methods and training content can vary, depending<br>on personnel roles.<br>**Examples**<br>Different methods that can be used to provide<br>security awareness and education include<br>posters, letters, web-based training, in-person<br>training, team meetings, and incentives.<br>Personnel acknowledgments may be recorded in<br>writing or electronically.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 311_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.6.3.1**Security awareness training includes<br>awareness of threats and vulnerabilities that could<br>impact the security of cardholder data and/or<br>sensitive authentication data, including but not<br>limited to:<br>•<br>Phishing and related attacks.<br>•<br>Social engineering.|**12.6.3.1**Examine security awareness training<br>content to verify it includes all elements specified in<br>this requirement.|Educating personnel on how to detect, react to,<br>and report potential phishing and related attacks<br>and social engineering attempts is essential to<br>minimizing the probability of successful attacks.<br>**Good Practice**<br>An effective security awareness program should<br>include examples of phishing emails and periodic<br>testing to determine the prevalence of personnel|
|**Customized Approach Objective**||reporting such attacks. Training material an entity<br>can consider for this topic include:|
|Personnel are knowledgeable about their own<br>human vulnerabilities and how threat actors will<br>attempt to exploit such vulnerabilities. Personnel are<br>able to access assistance and guidance when<br>required.||•<br>How to identify phishing and other social<br>engineering attacks.<br>•<br>How to react to suspected phishing and social<br>engineering.<br>•<br>Where and how to report suspected phishing|
|**Applicability Notes**||and social engineering activity.<br>An emphasis on reporting allows the organization|
|See Requirement 5.4.1 for guidance on the<br>difference between technical and automated<br>controls to detect and protect users from phishing<br>attacks, and this requirement for providing users<br>security awareness training about phishing and<br>social engineering. These are two separate and<br>distinct requirements, and one is not met by<br>implementing controls required by the other one.||to reward positive behavior, to optimize technical<br>defenses (see Requirement 5.4.1), and to take<br>immediate action to remove similar phishing<br>emails that evaded technical defenses from<br>recipient inboxes.|
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_|||
|_fully considered during a PCI DSS assessment._|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 312_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.6.3.2**Security awareness training includes<br>awareness about the acceptable use of end-user<br>technologies in accordance with Requirement<br>12.2.1.|**12.6.3.2**Examine security awareness training<br>content to verify it includes awareness about<br>acceptable use of end-user technologies in<br>accordance with Requirement 12.2.1.|By including the key points of the acceptable use<br>policy in regular training and the related context,<br>personnel will understand their responsibilities<br>and how these impact the security of an<br>organization’s systems.|
|**Customized Approach Objective**|||
|Personnel are knowledgeable about their<br>responsibility for the security and operation of end-<br>user technologies and are able to access assistance<br>and guidance when required.|||
|**Applicability Notes**|||
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 313_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

**12.7 Personnel are screened to reduce risks from insider threats.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.7.1**Potential personnel who will have access to<br>the CDE are screened, within the constraints of<br>local laws, prior to hire to minimize the risk of<br>attacks from internal sources.<br>**Customized Approach Objective**|**12.7.1**Interview responsible Human Resource<br>department management to verify that screening is<br>conducted, within the constraints of local laws,<br>prior to hiring potential personnel who will have<br>access to the CDE.|Performing thorough screening prior to hiring<br>potential personnel who are expected to be given<br>access to the CDE provides entities with the<br>information necessary to make informed risk<br>decisions regarding personnel they hire that will<br>have access to the CDE.<br>Other benefits of screening potential personnel|
|The risk related to allowing new members of staff<br>access to the CDE is understood and managed.||include helping to ensure workplace safety and<br>confirming information provided by prospective<br>employees on their resumes.|
|**Applicability Notes**||**Good Practice**<br>Entities should consider screening for existing|
|For those potential personnel to be hired for<br>positions such as store cashiers, who only have<br>access to one card number at a time when<br>facilitating a transaction, this requirement is a<br>recommendation only.||personnel anytime they transfer into roles where<br>they have access to the CDE from roles where<br>they did not have this access.<br>To be effective, the level of screening should be<br>appropriate for the position. For example,<br>positions requiring greater responsibility or that<br>have administrative access to critical data or<br>systems may warrant more detailed or more<br>frequent screening than positions with less<br>responsibility and access.<br>**Examples**<br>Screening options can include, as appropriate for<br>the entity’s region, previous employment history,<br>review of public information/social media<br>resources, criminal record, credit history, and<br>reference checks.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 314_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **12.8 Risk to information assets associated with third-party service provider (TPSP) relationships is managed.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.8.1**A list of all third-party service providers<br>(TPSPs) with which account data is shared or that<br>could affect the security of account data is<br>maintained, including a description for each of the<br>services provided.<br>**Customized Approach Objective**|**12.8.1.a**Examine policies and procedures to verify<br>that processes are defined to maintain a list of<br>TPSPs, including a description for each of the<br>services provided, for all TPSPs with whom<br>account data is shared or that could affect the<br>security of account data.<br>**12.8.1.b**Examine documentation to verify that a<br>list of all TPSPs is maintained that includes a<br>description of the services provided.|Maintaining a list of all TPSPs identifies where<br>potential risk extends outside the organization<br>and defines the organization’s extended attack<br>surface.<br>**Examples**<br>Different types of TPSPs include those that:<br>•<br>Store, process, or transmit account data on<br>the entity’s behalf (such as payment<br>gateways, payment processors, payment<br>service providers (PSPs), and off-site storage<br>providers).|
|Records are maintained of TPSPs and the services<br>provided.||•<br>Manage system components included in the<br>entity’s PCI DSS assessment (such as|
|**Applicability Notes**||providers of network security control services,<br>anti-malware services, and security incident|
|The use of a PCI DSS compliant TPSP does not<br>make an entity PCI DSS compliant, nor does it<br>remove the entity’s responsibility for its own PCI<br>DSS compliance.||and event management (SIEM); contact and<br>call centers; web-hosting companies; and<br>IaaS, PaaS, SaaS, and FaaS cloud<br>providers).<br>•<br>Could impact the security of the entity’s<br>cardholder data and/or sensitive<br>authentication data (such as vendors<br>providing support via remote access, and<br>bespoke software developers).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 315_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.8.2**Written agreements with TPSPs are<br>maintained as follows:<br>•<br>Written agreements are maintained with all<br>TPSPs with which account data is shared or that|**12.8.2.a**Examine policies and procedures to verify<br>that processes are defined to maintain written<br>agreements with all TPSPs in accordance with all<br>elements specified in this requirement.|The written acknowledgment from a TPSP<br>demonstrates its commitment to maintaining<br>proper security of account data that it obtains<br>from its customers and that the TPSP is fully<br>aware of the assets that could be affected during|
|could affect the security of the CDE.<br>•<br>Written agreements include acknowledgments<br>from TPSPs that TPSPs are responsible for the<br>security of account data the TPSPs possess or<br>otherwise store, process, or transmit on behalf<br>of the entity, or to the extent that the TPSP could|**12.8.2.b**Examine written agreements with TPSPs<br>to verify they are maintained in accordance with all<br>elements as specified in this requirement.|the provisioning of the TPSP’s service. The extent<br>to which a specific TPSP is responsible for the<br>security of account data will depend on the<br>service provided and the responsibilities agreed<br>between the provider and assessed entity (the<br>customer).|
|impact the security of the entity’s cardholder<br>data and/or sensitive authentication data.||In conjunction with Requirement 12.9.1, this<br>requirement is intended to promote a consistent<br>level of understanding between parties about their|
|**Customized Approach Objective**<br>Records are maintained of each TPSP’s<br>acknowledgment of its responsibility to protect<br>account data.||applicable PCI DSS responsibilities. For example,<br>the agreement may include the applicable PCI<br>DSS requirements to be maintained as part of the<br>provided service.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 316_ 



###### **Requirements and Testing Procedures** 

###### **Applicability Notes** 

The exact wording of an agreement will depend on the details of the service being provided, and the responsibilities assigned to each party. The agreement does not have to include the exact wording provided in this requirement. The TPSP’s written acknowledgment is a confirmation that states the TPSP is responsible for the security of the account data it may store, process, or transmit on behalf of the customer or to the extent the TPSP may impact the security of a customer’s cardholder data and/or sensitive authentication data. 

Evidence that a TPSP is meeting PCI DSS requirements (is not the same as a written acknowledgment specified in this requirement. For example, a PCI DSS Attestation of Compliance (AOC), a declaration on a company’s website, a policy statement, a responsibility matrix, or other evidence not included in a written agreement is not a written acknowledgment. 

###### **Guidance** 

###### **Good Practice** 

The entity may also want to consider including in their written agreement with a TPSP that the TPSP will support the entity’s request for information per Requirement 12.9.2. Entities will also want to understand whether any TPSPs have “nested” relationships with other TPSPs, meaning the primary TPSP contracts with another TPSP(s) for the purposes of providing a service. It is important to understand whether the primary TPSP is relying on the secondary TPSP(s) to achieve overall compliance of a service, and what types of written agreements the primary TPSP has in place with the secondary TPSPs. Entities can consider including coverage in their written agreement for any “nested” TPSPs a primary TPSP may use. 

###### **Further Information** 

Refer to the _Information Supplement: Third-Party Security Assurance_ for further guidance. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 317_ 



###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.8.3**An established process is implemented for<br>engaging TPSPs, including proper due diligence<br>prior to engagement.|**12.8.3.a**Examine policies and procedures to verify<br>that processes are defined for engaging TPSPs,<br>including proper due diligence prior to<br>engagement.|A thorough process for engaging TPSPs,<br>including details for selection and vetting prior to<br>engagement, helps ensure that a TPSP is<br>thoroughly vetted internally by an entity prior to<br>establishing a formal relationship and that the risk|
|**Customized Approach Objective**|**12.8.3.b**Examine evidence and interview<br>responsible personnel to verify the process for<br>engaging TPSPs includes proper due diligence<br>prior to engagement.|to cardholder data associated with the<br>engagement of the TPSP is understood.<br>**Good Practice**<br>Specific due-diligence processes and goals will|
|The capability, intent, and resources of a<br>prospective TPSP to adequately protect account<br>data are assessed before the TPSP is engaged.||vary for each organization. Elements that should<br>be considered include the provider’s reporting<br>practices, breach-notification and incident<br>response procedures, details of how PCI DSS<br>responsibilities are assigned between each party,<br>how the TPSP validates their PCI DSS<br>compliance and what evidence they provide.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 318_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**12.8.4**A program is implemented to monitor TPSPs’<br>PCI DSS compliance status at least once every 12<br>months.|**12.8.4.a**Examine policies and procedures to verify<br>that processes are defined to monitor TPSPs’ PCI<br>DSS compliance status at least once every 12<br>months.|Knowing the PCI DSS compliance status of all<br>engaged TPSPs provides assurance and awareness<br>about whether they comply with the requirements<br>applicable to the services they offer to the<br>organization.|
||**12.8.4.b**Examine documentation and interview<br>responsible personnel to verify that the PCI DSS|**Good Practice**<br>If the TPSP offers a variety of services, the|
|**Customized Approach Objective**<br>The PCI DSS compliance status of TPSPs is verified<br>periodically.|<br>compliance status of each TPSP is monitored at least<br>once every 12 months.|compliance status the entity monitors should be<br>specific to those services delivered to the entity and<br>those services in scope for the entity’s PCI DSS<br>assessment.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 319_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Applicability Notes**<br>Where an entity has an agreement with a TPSP for<br>meeting PCI DSS requirements on behalf of the<br>entity (for example, via a firewall service), the entity<br>must work with the TPSP to make sure the<br>applicable PCI DSS requirements are met. If the<br>TPSP does not meet those applicable PCI DSS<br>requirements, then those requirements are also “not<br>in place” for the entity.|If a TPSP has a PCI DSS Attestation of<br>Compliance (AOC), the expectation is that the<br>TPSP should provide that to customers upon<br>request to demonstrate their PCI DSS compliance<br>status.<br>If the TPSP did not undergo a PCI DSS<br>assessment, it may be able to provide other<br>sufficient evidence to demonstrate that it has met<br>the applicable requirements without undergoing a<br>formal compliance validation. For example, the<br>TPSP can provide specific evidence to the entity’s<br>assessor so the assessor can confirm applicable<br>requirements are met. Alternatively, the TPSP<br>can elect to undergo multiple on-demand<br>assessments by each of its customers’ assessors,<br>with each assessment targeted to confirm that<br>applicable requirements are met.<br>**Further Information**<br>For more information about third-party service<br>providers, refer to:<br>•<br>PCI DSS section: Use of Third-Party Service<br>Providers.<br>•<br>_Information Supplement: Third-Party Security_<br>_Assurance_.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 320_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.8.5**Information is maintained about which PCI<br>DSS requirements are managed by each TPSP,<br>which are managed by the entity, and any that are<br>shared between the TPSP and the entity.|**12.8.5.a**Examine policies and procedures to verify<br>that processes are defined to maintain information<br>about which PCI DSS requirements are managed<br>by each TPSP, which are managed by the entity,<br>and any that are shared between both the TPSP<br>and the entity.|It is important that the entity understands which<br>PCI DSS requirements and sub-requirements its<br>TPSPs have agreed to meet, which requirements<br>are shared between the TPSP and the entity, and<br>for those that are shared, specifics about how the<br>requirements are shared and which entity is<br>responsible for meeting each sub-requirement.|
||**12.8.5.b**Examine documentation and interview<br>ersonnel to verif the entit maintains information|Without this shared understanding, it is inevitable<br>that the entity and the TPSP will assume a given|
|**Customized Approach Objective**|p  y  y<br>about which PCI DSS requirements are managed<br>by each TPSP which are managed by the entity|PCI DSS sub-requirement is the responsibility of<br>the other party, and therefore that sub-|
|Records detailing the PCI DSS requirements and<br>related system components for which each TPSP is<br>solely or jointly responsible, are maintained and<br>reviewed periodically.|,      ,<br>and any that are shared between both entities.|requirement may not be addressed at all.<br>The specific information an entity maintains will<br>depend on the particular agreement with their<br>providers, the type of service, etc. TPSPs may<br>define their PCI DSS responsibilities to be the<br>same for all their customers; otherwise, this<br>responsibility should be agreed upon by both the<br>entity and TPSP.<br>**Good Practice**|
|||Entities can document these responsibilities via a<br>matrix that identifies all applicable PCI DSS<br>requirements and indicates for each requirement<br>whether the entity or TPSP is responsible for<br>meeting that requirement or whether it is a shared<br>responsibility. This type of document is often<br>referred to as a_responsibility matrix_.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 321_ 



||**Requirements and Testing Procedures**|**Guidance**|
|---|---|---|
|**12.8.5** _(continued)_||It is also important for entities to understand<br>whether any TPSPs have “nested” relationships<br>with other TPSPs, meaning the primary TPSP<br>contracts with another TPSP(s) for the purposes<br>of providing a service. It is important to<br>understand whether the primary TPSP is relying<br>on the secondary TPSP(s) to achieve overall<br>compliance of a service, and how the primary<br>TPSP is monitoring performance of the service<br>and the PCI DSS compliance status of the<br>secondary TPSP(s). Note that it is the<br>responsibility of the primary TPSP to manage and<br>monitor any secondary TPSPs.<br>**Further Information**<br>Refer to_Information Supplement: Third-Party_<br>_Security Assurance_for a sample responsibility<br>matrix template.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 June 2024 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved. Page 322_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **12.9 Third-party service providers (TPSPs) support their customers’ PCI DSS compliance.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.9.1** **_Additional requirement for service_**<br>**_providers only:_**TPSPs provide written agreements<br>to customers that include acknowledgments that<br>TPSPs are responsible for the security of account<br>data the TPSP possesses or otherwise stores,<br>processes, or transmits on behalf of the customer,<br>or to the extent that the TPSP could impact the<br>security of the customer’s cardholder data and/or<br>sensitive authentication data.|**12.9.1** **_Additional testing procedure for service_**<br>**_provider assessments only:_**Examine TPSP<br>policies, procedures, and templates used for<br>written agreements to verify processes are defined<br>for the TPSP to provide written acknowledgments<br>to customers in accordance with all elements<br>specified in this requirement.|In conjunction with Requirement 12.8.2, this<br>requirement is intended to promote a consistent<br>level of understanding between TPSPs and their<br>customers about their applicable PCI DSS<br>responsibilities. The acknowledgment from the<br>TPSP evidences the TPSP’s commitment to<br>maintaining proper security of the account data<br>that it obtains from its customers.<br>The TPSP’s internal policies and procedures<br>related to their customer engagement process|
|**Customized Approach Objective**||and any templates used for written agreements<br>should include provision of an applicable PCI|
|TPSPs formally acknowledge their security<br>responsibilities to their customers.<br>_(continued on next page)_||DSS acknowledgement to its customers. The<br>method by which the TPSP provides written<br>acknowledgment should be agreed between the<br>provider and its customers.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 323_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**Applicability Notes**||
|This requirement applies only when the entity being<br>assessed is a service provider.||
|The exact wording of an agreement will depend on<br>the details of the service being provided, and the<br>responsibilities assigned to each party. The<br>agreement does not have to include the exact<br>wording provided in this requirement.<br>The TPSP’s written acknowledgment is a<br>confirmation that states the TPSP is responsible for<br>the security of the account data it may store,<br>process, or transmit on behalf of the customer or to<br>the extent the TPSP may impact the security of a<br>customer’s cardholder data and/or sensitive<br>authentication data.||
|Evidence that a TPSP is meeting PCI DSS<br>requirements is not the same as a written<br>agreement specified in this requirement. For<br>example, a PCI DSS Attestation of Compliance<br>(AOC), a declaration on a company’s website, a<br>policy statement, a responsibility matrix, or other<br>evidence not included in a written agreement is not<br>a written acknowledgment.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 324_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.9.2** **_Additional requirement for service_**<br>**_providers only:_**TPSPs support their customers’<br>requests for information to meet Requirements<br>12.8.4 and 12.8.5 by providing the following upon<br>customer request:<br>•<br>PCI DSS compliance status information<br>(Requirement 12.8.4).<br>•<br>Information about which PCI DSS requirements<br>are the responsibility of the TPSP and which are<br>the responsibility of the customer, including any<br>shared responsibilities (Requirement 12.8.5), for<br>any service the TPSP provides that meets a PCI<br>DSS requirement(s) on behalf of customers or<br>that can impact security of customers’<br>cardholder data or sensitive authentication data.|**12.9.2** **_Additional testing procedure for service_**<br>**_provider assessments only:_**Examine policies<br>and procedures to verify processes are defined for<br>the TPSPs to support customers’ request for<br>information to meet Requirements 12.8.4 and<br>12.8.5 in accordance with all elements specified in<br>this requirement.|If a TPSP does not provide the necessary<br>information to enable its customers to meet their<br>security and compliance requirements, the<br>customers will not be able to protect cardholder<br>data nor meet their own contractual obligations.<br>**Good Practice**<br>If a TPSP has a PCI DSS Attestation of<br>Compliance (AOC), the expectation is that the<br>TPSP should provide that to customers upon<br>request to demonstrate their PCI DSS compliance<br>status.<br>If the TPSP did not undergo a PCI DSS<br>assessment, they may be able to provide other<br>sufficient evidence to demonstrate that it has met<br>the applicable requirements without undergoing a<br>formal compliance validation. For example, the|
|**Customized Approach Objective**||TPSP can provide specific evidence to the entity’s<br>assessor so the assessor can confirm applicable|
|TPSPs provide information as needed to support<br>their customers’ PCI DSS compliance efforts.||requirements are met. Alternatively, the TPSP<br>can elect to undergo multiple on-demand<br>assessments by each of its customers’ assessors,|
|**Applicability Notes**||with each assessment targeted to confirm that<br>applicable requirements are met.|
|This requirement applies only when the entity being<br>assessed is a service provider.||TPSPs should provide sufficient evidence to their<br>customers to verify that the scope of the TPSP’s<br>PCI DSS assessment covered the services<br>applicable to the customer and that the relevant<br>PCI DSS requirements were examined and<br>determined to be in place.|
|||_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 325_ 



|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|**12.9.2**_(continued)_|TPSPs may define their PCI DSS responsibilities<br>to be the same for all their customers; otherwise,<br>this responsibility should be agreed upon by both<br>the customer and TPSP. It is important that the<br>customer understands which PCI DSS<br>requirements and sub-requirements its TPSPs<br>have agreed to meet, which requirements are<br>shared between the TPSP and the customer, and<br>for those that are shared, specifics about how the<br>requirements are shared and which entity is<br>responsible for meeting each sub-requirement. An<br>example of a way to document these<br>responsibilities is via a matrix that identifies all<br>applicable PCI DSS requirements and indicates<br>whether the customer or TPSP is responsible for<br>meeting that requirement or whether it is a shared<br>responsibility.<br>**Further Information**<br>For further guidance, refer to:<br>•<br>PCI DSS section:_Use of Third-Party Service_<br>_Providers_.<br>•<br>_Information Supplement: Third-Party Security_<br>_Assurance_(includes a sample responsibility<br>matrix template).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 326_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**12.10** **Suspected and confirmed security inciden**|**ts that could impact the CDE are responded to**|**immediately.**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**12.10.1**An incident response plan exists and is<br>ready to be activated in the event of a suspected or<br>confirmed security incident. The plan includes, but is<br>not limited to:|**12.10.1.a**Examine the incident response plan to<br>verify that the plan exists and includes at least the<br>elements specified in this requirement.|Without a comprehensive incident response plan<br>that is properly disseminated, read, and<br>understood by the parties responsible, confusion<br>and lack of a unified response could create further<br>downtime for the business, unnecessary public|
|•<br>Roles, responsibilities, and communication and<br>contact strategies in the event of a suspected or<br>confirmed security incident, including notification<br>of payment brands and acquirers, at a minimum.<br>•<br>Incident response procedures with specific<br>containment and mitigation activities for different<br>types of incidents.|**12.10.1.b**Interview personnel and examine<br>documentation from previously reported incidents<br>or alerts to verify that the documented incident<br>response plan and procedures were followed.|media exposure, as well as risk of financial and/or<br>reputational loss and legal liabilities.<br>**Good Practice**<br>The incident response plan should be thorough<br>and contain all the key elements for stakeholders<br>(for example, legal, communications) to allow the<br>entity to respond effectively in the event of a|
|•<br>Business recovery and continuity procedures.||breach that could impact account data. It is|
|•<br>Data backup processes.<br>•<br>Analysis of legal requirements for reporting<br>compromises.<br>||important to keep the plan up to date with current<br>contact information of all individuals designated<br>as having a role in incident response. Other<br>relevant parties for notifications may include|
|•<br>Coverage and responses of all critical system<br>components.||<br>customers, financial institutions (acquirers and<br>issuers), and business partners.|
|•<br>Reference or inclusion of incident response<br>procedures from the payment brands.||Entities should consider how to address all<br>compromises of data within the CDE in their|
|**Customized Approach Objective**||incident response plans, including compromises<br>to account data, wireless encryption keys,|
|A comprehensive incident response plan that meets<br>card brand expectations is maintained.||encryption keys used for transmission and<br>storage or account data or cardholder data, etc.<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 327_ 



###### **Requirements and Testing Procedures Guidance** 

|**12.10.1**_(continued)_||**Examples**<br>Legal requirements for reporting compromises<br>include those in most US states, the EU General<br>Data Protection Regulation (GDPR), and the<br>Personal Data Protection Act (Singapore).<br>**Further Information**<br>For more information, refer to the_NIST SP 800-_<br>_61 Rev. 2, Computer Security Incident Handling_<br>_Guide_.|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**12.10.2**At least once every 12 months, the security<br>incident response plan is:<br>•<br>Reviewed and the content is updated as<br>needed.<br>•<br>Tested, including all elements listed in<br>Requirement 12.10.1.|**12.10.2**Interview personnel and review<br>documentation to verify that, at least once every 12<br>months, the security incident response plan is:<br>•<br>Reviewed and updated as needed.<br>•<br>Tested, including all elements listed in<br>Requirement 12.10.1.|Proper testing of the security incident response<br>plan can identify broken business processes and<br>ensure key steps are not missed, which could<br>result in increased exposure during an incident.<br>Periodic testing of the plan ensures that the<br>processes remain viable, as well as ensuring that<br>all relevant personnel in the organization are<br>familiar with the plan.|
|**Customized Approach Objective**||**Good Practice**|
|The incident response plan is kept current and<br>tested periodically.||The test of the incident response plan can include<br>simulated incidents and the corresponding<br>responses in the form of a “table-top exercise”<br>that includes participation by relevant personnel.<br>A review of the incident and the quality of the<br>response can provide entities with the assurance<br>that all required elements are included in the plan.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 328_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.10.3**Specific personnel are designated to be<br>available on a 24/7 basis to respond to suspected or<br>confirmed security incidents.|**12.10.3**Examine documentation and interview<br>responsible personnel occupying designated roles<br>to verify that specific personnel are designated to<br>be available on a 24/7 basis to respond to security|An incident could occur at any time, therefore if a<br>person who is trained in incident response and<br>familiar with the entity’s plan is available when an<br>incident is detected, the entity’s ability to correctly<br>|
|**Customized Approach Objective**|<br>incidents.|respond to the incident is increased.<br>**Good Practice**|
|Incidents are responded to immediately where<br>appropriate.||Often, specific personnel are designated to be<br>part of a security incident response team, with the<br>team having overall responsibility for responding<br>to incidents (perhaps on a rotating schedule<br>basis) and managing those incidents in<br>accordance with the plan. The incident response<br>team can consist of core members who are<br>permanently assigned or “on-demand” personnel<br>who may be called up as necessary, depending<br>on their expertise and the specifics of the incident.<br>Having available resources to respond quickly to<br>incidents minimizes disruption to the organization.<br>Examples of types of activity the team or<br>individuals should respond to include any<br>evidence of unauthorized activity, detection of<br>unauthorized wireless access points, critical IDS<br>alerts, and reports of unauthorized critical system<br>or content file changes.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 329_ 



|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**12.10.4**Personnel responsible for responding to<br>suspected and confirmed security incidents are<br>appropriately and periodically trained on their<br>incident response responsibilities.|**12.10.4**Examine training documentation and<br>interview incident response personnel to verify that<br>personnel are appropriately and periodically<br>trained on their incident response responsibilities.|Without a trained and readily available incident<br>response team, extended damage to the network<br>could occur, and critical data and systems may<br>become “polluted” by inappropriate handling of<br>the targeted systems. This can hinder the<br>|
|**Customized Approach Objective**||success of a post-incident investigation.<br>**Good Practice**|
|Personnel are knowledgeable about their role and<br>responsibilities in incident response and are able to<br>access assistance and guidance when required.||It is important that all personnel involved in<br>incident response are trained and knowledgeable<br>about managing evidence for forensics and<br>investigations.|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**12.10.4.1**The frequency of periodic training for<br>incident response personnel is defined in the<br>entity’s targeted risk analysis, which is performed<br>according to all elements specified in Requirement<br>12.3.1.|**12.10.4.1.a**Examine the entity’s targeted risk<br>analysis for the frequency of training for incident<br>response personnel to verify the risk analysis was<br>performed in accordance with all elements<br>specified in Requirement 12.3.1.|Each entity’s environment and incident response<br>plan are different, and the approach will depend<br>on a number of factors, including the size and<br>complexity of the entity, the degree of change in<br>the environment, the size of the incident response<br>team, and the turnover in personnel.|
|**Customized Approach Objective**<br>Incident response personnel are trained at a<br>frequency that addresses the entity’s risk.|**12.10.4.1.b**Examine documented results of<br>periodic training of incident response personnel<br>and interview personnel to verify training is<br>performed at the frequency defined in the entity’s<br>targeted risk analysis performed for this<br>requirement.|Performing a risk analysis will allow the entity to<br>determine the optimum frequency for training<br>personnel with incident response responsibilities.|
|**Applicability Notes**|||
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 330_ 



###### **Requirements and Testing Procedures** 

- **Defined Approach Requirements Defined Approach Testing Procedures 12.10.5** The security incident response plan **12.10.5** Examine documentation and observe includes monitoring and responding to alerts from incident response processes to verify that security monitoring systems, including but not monitoring and responding to alerts from security limited to: monitoring systems are covered in the security • Intrusion-detection and intrusion-prevention incident response plan, including but not limited to systems. the systems specified in this requirement. 

- • Network security controls. • Change-detection mechanisms for critical files. • The change-and tamper-detection mechanism for payment pages. _This bullet is a best practice until its effective date; refer to Applicability Notes below for details._ 

- • Detection of unauthorized wireless access points. 

###### **Guidance** 

###### **Purpose** 

Responding to alerts generated by security monitoring systems that are explicitly designed to focus on potential risk to data is critical to prevent a breach and therefore, this must be included in the incident-response processes. 

###### **Customized Approach Objective** 

Alerts generated by monitoring and detection technologies are responded to in a structured, repeatable manner. **Applicability Notes** 

_The bullet above (for monitoring and responding to alerts from a change- and tamper-detection mechanism for payment pages) is a best practice until 31 March 2025, after which it will be required as part of Requirement 12.10.5 and must be fully considered during a PCI DSS assessment._ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 331_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.10.6**The security incident response plan is<br>modified and evolved according to lessons learned<br>and to incorporate industry developments.|**12.10.6.a**Examine policies and procedures to<br>verify that processes are defined to modify and<br>evolve the security incident response plan<br>according to lessons learned and to incorporate<br>industry developments.|Incorporating lessons learned into the incident<br>response plan after an incident occurs and in-step<br>with industry developments, helps keep the plan<br>current and able to react to emerging threats and<br>security trends.<br>**Good Practice**|
||**12.10.6.b**Examine the security incident response<br>plan and interview responsible personnel to verify|The lessons-learned exercise should include all<br>levels of personnel. Although it is often included|
|**Customized Approach Objective**|<br>that the incident response plan is modified and<br>evolved according to lessons learned and to|as part of the review of the entire incident, it<br>should focus on how the entity’s response to the|
|The effectiveness and accuracy of the incident<br>response plan is reviewed and updated after each<br>invocation.|<br>incorporate industry developments.|incident could be improved.<br>It is important to not just consider elements of the<br>response that did not have the planned outcomes<br>but also to understand what worked well and<br>whether lessons from those elements that worked<br>well can be applied to areas of the plan that did<br>not.<br>Another way to optimize an entity’s incident<br>response plan is to understand the attacks made<br>against other organizations and use that<br>information to fine-tune the entity’s detection,<br>containment, mitigation, or recovery procedures.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 332_ 



###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**12.10.7**Incident response procedures are in place,<br>to be initiated upon the detection of stored PAN<br>anywhere it is not expected, and include:<br>•<br>Determining what to do if PAN is discovered<br>outside the CDE, including its retrieval, secure<br>|**12.10.7.a**Examine documented incident response<br>procedures to verify that procedures for responding<br>to the detection of stored PAN anywhere it is not<br>expected to exist, ready to be initiated, and include<br>all elements specified in this requirement.|Having documented incident response<br>procedures that are followed in the event that<br>stored PAN is found anywhere it is not expected<br>to be, helps to identify the necessary remediation<br>actions and prevent future leaks.<br>**Good Practice**|
|deletion, and/or migration into the currently<br>defined CDE, as applicable.<br>•<br>Identifying whether sensitive authentication data<br>is stored with PAN.<br>•<br>Determining where the account data came from<br>and how it ended up where it was not expected.<br>•<br>Remediating data leaks or process gaps that<br>resulted in the account data being where it was<br>not expected.<br>**Customized Approach Objective**<br>Processes are in place to quickly respond, analyze,<br>and address situations in the event that cleartext<br>PAN is detected where it is not expected.|**12.10.7.b**Interview personnel and examine<br>records of response actions to verify that incident<br>response procedures are performed upon<br>detection of stored PAN anywhere it is not<br>expected.|If PAN was found outside the CDE, analysis<br>should be performed to 1) determine whether it<br>was saved independently of other data or with<br>sensitive authentication data, 2) identify the<br>source of the data, and 3) identify the control<br>gaps that resulted in the data being outside the<br>CDE.<br>Entities should consider whether there are<br>contributory factors, such as business processes,<br>user behavior, improper system configurations,<br>etc. that caused the PAN to be stored in an<br>unexpected location. If such contributory factors<br>are present, they should be addressed per this<br>Requirement to prevent recurrence.|
|**Applicability Notes**|||
|_This requirement is a best practice until 31 March_<br>_2025, after which it will be required and must be_<br>_fully considered during a PCI DSS assessment._|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 ©2006 - 2024 PCI Security Standards Council, LLC. All Rights Reserved._ 

_June 2024 Page 333_ 

## **Appendix A Additional PCI DSS Requirements** 

This appendix contains additional PCI DSS requirements for different types of entities. The sections within this Appendix include: 

- Appendix A1:  Additional PCI DSS Requirements for Multi-Tenant Service Providers 

- Appendix A2:  Additional PCI DSS Requirements for Entities Using SSL/early TLS for Card-Present POS POI Terminal Connections 

- Appendix A3:  Designated Entities Supplemental Validation (DESV) 

Guidance and applicability information is provided in each section. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 334_ 

#### **_Appendix A1: Additional PCI DSS Requirements for Multi-Tenant Service Providers_** 

###### **Sections** 

**A1.1** Multi-tenant service providers protect and separate all customer environments and data. 

**A1.2** Multi-tenant service providers facilitate logging and incident response for all customers. 

###### **Overview** 

All service providers are responsible for meeting PCI DSS requirements for their own environments as applicable to the services offered to their customers. In addition, multi-tenant service providers must meet the requirements in this Appendix. 

Multi-tenant service providers are a type of third-party service provider that offers various shared services to merchants and other service providers, where customers share system resources (such as physical or virtual servers), infrastructure, applications (including Software as a Service (SaaS)), and/or databases. Services may include, but are not limited to, hosting multiple entities on a single shared server, providing e-commerce and/or “shopping cart” services, webbased hosting services, payment applications, various cloud applications and services, and  payment gateway and processor services offered in a shared environment. 

Service providers that provide only shared data center services (often called co-location or “co-lo” providers), where equipment, space, and bandwidth are available on a rental basis, are not considered multi-tenant service providers for purposes of this Appendix. 

**_<mark>Note</mark>_** _<mark>: Even though a multi-tenant service provider may meet these requirements, each customer is still responsible to comply with the PCI DSS requirements that are applicable to its environment and validate compliance as applicable. Often, there are PCI DSS requirements for which responsibility is shared between the provider and the customer (for perhaps different aspects of the environment). Requirements 12.8 and 12.9 delineate requirements specific to the relationships between all third-party service providers (TPSPs) and their customers, and the responsibilities of both. This includes defining the specific services the customer is receiving, along with which PCI DSS requirements are the responsibility of the customer to meet, which are the responsibility of the TPSP, and which requirements are shared between both customer and the TPSP.</mark>_ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 335_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

**A1.1 Multi-tenant service providers protect and separate all customer environments and data.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A1.1.1**Logical separation is implemented as<br>follows:<br>•<br>The provider cannot access its customers’<br>environments without authorization.<br>•<br>Customers cannot access the provider’s<br>environment without authorization.|**A1.1.1**Examine documentation and system and<br>network configurations and interview personnel to<br>verify that logical separation is implemented in<br>accordance with all elements specified in this<br>requirement.|Without controls between the provider’s environment<br>and the customer’s environment, a malicious actor<br>within the provider’s environment could compromise<br>the customer’s environment, and similarly, a<br>malicious actor in a customer environment could<br>compromise the provider and potentially other of the<br>provider’s customers.<br>Multi-tenant environments should be isolated from|
|**Customized Approach Objective**||each other and from the provider’s infrastructure<br>such that they can be separately managed entities|
|Customers cannot access the provider’s<br>environment. The provider cannot access its<br>customers’ environments without authorization.||with no connectivity between them.<br>**Good Practice**<br>Providers should ensure strong separation between<br>the environments that are designed for customer<br>access, for example, configuration and billing portals,|
|**Applicability Notes**||and the provider’s private environment that should<br>only be accessed by authorized provider personnel.|
|_This requirement is a best practice until 31_<br>_March 2025, after which it will be required and_<br>_must be fully considered during a PCI DSS_||Service provider access to customer environments is<br>performed in accordance with requirement 8.2.3.<br>**Further Information**|
|_assessment._||Refer to the_Information Supplement: PCI SSC Cloud_<br>_Computing Guidelines_for further guidance on cloud<br>environments.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 336_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A1.1.2**Controls are implemented such that each<br>customer only has permission to access its own<br>cardholder data and CDE.|**A1.1.2.a**Examine documentation to verify controls<br>are defined such that each customer only has<br>permission to access its own cardholder data and<br>CDE.|It is important that a multi-tenant service provider<br>define controls so that each customer can only<br>access their own environment and CDE to prevent<br>unauthorized access from one customer’s<br>environment to another.|
|**Customized Approach Objective**|**A1.1.2.b**Examine system configurations to verify<br>that customers have privileges established to only<br>access their own account data and CDE.|**Examples**<br>In a cloud-based infrastructure, such as an<br>infrastructure as a service (IaaS) offering, the<br>customers’ CDE may include virtual network devices|
|Customers cannot access other customers’<br>environments.||and virtual servers that are configured and managed<br>by the customers, including operating systems, files,<br>memory, etc.|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**A1.1.3**Controls are implemented such that each<br>customer can only access resources allocated to<br>them.|**A1.1.3**Examine customer privileges to verify each<br>customer can only access resources allocated to<br>them.|To prevent any inadvertent or intentional impact to<br>other customers’ environments or account data, it is<br>important that each customer can access only<br>resources allocated to that customer.|
|**Customized Approach Objective**|||
|Customers cannot impact resources allocated to<br>other customers.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 337_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A1.1.4**The effectiveness of logical separation<br>controls used to separate customer<br>environments is confirmed at least once every<br>six months via penetration testing.|**A1.1.4**Examine the results from the most recent<br>penetration test to verify that testing confirmed the<br>effectiveness of logical separation controls used to<br>separate customer environments.|Multi-tenant services providers are responsible for<br>managing the segmentation between their<br>customers.<br>Without technical assurance that segmentation<br>controls are effective, it is possible that changes to|
|**Customized Approach Objective**||the service provider’s technology would inadvertently<br>create a vulnerability that could be exploited across|
|Segmentation of customer environments from<br>other environments is periodically validated to be||all the service provider’s customers.<br>**Good Practice**|
|effective.<br>**Applicability Notes**<br>The testing of adequate separation between<br>customers in a multi-tenant service provider<br>environment is in addition to the penetration<br>tests specified in Requirement 11.4.6.||Effectiveness of separation techniques can be<br>confirmed by using service-provider-created<br>temporary (mock-up) environments that represent<br>customer environments and attempting to 1) access<br>one temporary environment from another<br>environment, and 2) access a temporary environment<br>from the Internet.|
|_This requirement is a best practice until 31_<br>_March 2025, after which it will be required and_<br>_must be fully considered during a PCI DSS_<br>_assessment._|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 338_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **A1.2 Multi-tenant service providers facilitate logging and incident response for all customers.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A1.2.1**Audit log capability is enabled for each<br>customer’s environment that is consistent with<br>PCI DSS Requirement 10, including:<br>•<br>Logs are enabled for common third-party<br>applications.|**A1.2.1**Examine documentation and system<br>configuration settings to verify the provider has<br>enabled audit log capability for each customer<br>environment in accordance with all elements<br>specified in this requirement.|Log information is useful for detecting and<br>troubleshooting security incidents and is invaluable<br>for forensic investigations. Customers therefore need<br>to have access to these logs.<br>However, log information can also be used by an<br>attacker for reconnaissance, and so a customer’s log|
|•<br>Logs are active by default.<br>•<br>Logs are available for review only by the<br>owning customer.||information must only be accessible by the customer<br>that the log relates to.|
|•<br>Log locations are clearly communicated to|||
|the owning customer.|||



|•<br>Log data and availability is consistent with<br>PCI DSS Requirement 10.|
|---|
|**Customized Approach Objective**|
|Log capability is available to all customers<br>without affecting the confidentiality of other<br>customers.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 339_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A1.2.2**Processes or mechanisms are<br>implemented to support and/or facilitate prompt<br>forensic investigations in the event of a<br>suspected or confirmed security incident for any<br>customer.<br>**Customized Approach Objective**|**A1.2.2**Examine documented procedures to verify<br>that the provider has processes or mechanisms to<br>support and/or facilitate a prompt forensic<br>investigation of related servers in the event of a<br>suspected or confirmed security incident for any<br>customer.|In the event of a suspected or confirmed breach of<br>confidentiality of cardholder data, a customer’s<br>forensic investigator aims to find the cause of the<br>breach, exclude the attacker from the environment,<br>and ensure all unauthorized access is removed.<br>Prompt and efficient responses to forensic<br>investigators’ requests can significantly reduce the<br>time taken for the investigator to secure the|
|Forensic investigation is readily available to all<br>customers in the event of a suspected or<br>confirmed security incident.||customer’s environment.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 340_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A1.2.3**Processes or mechanisms are<br>implemented for reporting and addressing<br>suspected or confirmed security incidents and<br>vulnerabilities, including:<br>•<br>Customers can securely report security<br>incidents and vulnerabilities to the provider.|**A1.2.3**Examine documented procedures and<br>interview personnel to verify that the provider has a<br>mechanism for reporting and addressing<br>suspected or confirmed security incidents and<br>vulnerabilities, in accordance with all elements<br>specified in this requirement.|Security vulnerabilities in the provided services can<br>impact the security of all the service provider’s<br>customers and therefore must be managed in<br>accordance with the service provider’s established<br>processes, with priority given to resolving<br>vulnerabilities that have the highest probability of<br>compromise.|
|•<br>The provider addresses and remediates<br>suspected or confirmed security incidents<br>and vulnerabilities according to Requirement<br>6.3.1.||Customers are likely to notice vulnerabilities and<br>security misconfigurations while using the service.<br>Implementing secure methods for customers to<br>report security incidents and vulnerabilities|
|**Customized Approach Objective**<br>Suspected or confirmed security incidents or<br>vulnerabilities are discovered and addressed.<br>Customers are informed where appropriate.||encourages customers to report potential issues and<br>enable the provider to quickly learn about and<br>address potential issues within their environment.|
|**Applicability Notes**|||
|_This requirement is a best practice until 31_<br>_March 2025, after which it will be required and_<br>_must be fully considered during a PCI DSS_<br>_assessment._|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 341_ 

#### **_Appendix A2: Additional PCI DSS Requirements for Entities Using SSL/Early TLS for Card-Present POS POI Terminal Connections_** 

###### **Sections** 

**A2.1** POI terminals using SSL and/or early TLS are confirmed as not susceptible to known SSL/TLS exploits. 

###### **Overview** 

This Appendix applies only to entities using SSL/early TLS as a security control to protect POS POI terminals, including service providers that provide connections into POS POI terminals. 

Entities using SSL and early TLS for POS POI terminal connections must work toward upgrading to a strong cryptographic protocol as soon as possible. Additionally, SSL and/or early TLS must not be introduced into environments where those protocols don’t already exist. At the time of publication, the known vulnerabilities are difficult to exploit in POS POI payment terminals. However, new vulnerabilities could emerge at any time, and it is up to the organization to remain up to date with vulnerability trends and determine whether it is susceptible to any known exploits. The PCI DSS requirements directly affected are: 

- **Requirement 2.2.5** : Where any insecure services, protocols, or daemons are present; business justification is documented, and additional security features are documented and implemented that reduce the risk of using insecure services, protocols, or daemons. 

- **Requirement 2.2.7** : All non-console administrative access is encrypted using strong cryptography. 

- **Requirement 4.2.1** : Strong cryptography and security protocols are implemented to safeguard PAN during transmission over open, public networks. 

SSL and early TLS must not be used as a security control to meet these requirements, except in the case of POS POI terminal connections, as detailed in this appendix. To support entities working to migrate from SSL/early TLS on POS POI terminals, the following provisions are included: 

- New POS POI terminal implementations must not use SSL or early TLS as a security control. 

- All POS POI terminal service providers must provide a secure service offering. 

- Service providers supporting existing POS POI terminal implementations that use SSL and/or early TLS must have a formal Risk Mitigation and Migration Plan in place. 

- POS POI terminals in card-present environments that can be verified as not being susceptible to any known exploits for SSL and early TLS, **and the SSL/TLS termination points to which they connect** , may continue using SSL/early TLS as a security control. 

Requirements in this Appendix are not eligible for the Customized Approach. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 342_ 

###### **Requirements and Testing Procedures Guidance A2.1 POI terminals using SSL and/or early TLS are confirmed as not susceptible to known SSL/TLS exploits.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A2.1.1**Where POS POI terminals at the merchant<br>or payment acceptance location use SSL and/or<br>early TLS, the entity confirms the devices are not<br>susceptible to any known exploits for those<br>protocols.|**A2.1.1**For POS POI terminals using SSL and/or<br>early TLS, confirm the entity has documentation (for<br>example, vendor documentation, system/network<br>configuration details) that verifies the devices are not<br>susceptible to any known exploits for SSL/early TLS.|POS POI terminals used in card-present<br>environments can continue using SSL/early TLS<br>when it can be shown that the POS POI terminal<br>is not susceptible to the currently known exploits.<br>**Good Practice**<br>However, SSL is outdated technology and could|
|**Customized Approach Objective**||be susceptible to additional security vulnerabilities<br>in the future; it is therefore strongly recommended|
|This requirement is not eligible for the customized<br>approach.||that POS POI terminals be upgraded to a secure<br>protocol as soon as possible. If SSL/early TLS is<br>not needed in the environment, use of, and|
|**Applicability Notes**||fallback to these versions should be disabled.<br>**Further Information**|
|This requirement is intended to apply to the entity<br>with the POS POI terminal, such as a merchant.<br>This requirement is not intended for service<br>||Refer to the current PCI SSC Information<br>Supplements on SSL/Early TLS for further<br>guidance.|



This requirement is intended to apply to the entity with the POS POI terminal, such as a merchant. This requirement is not intended for service providers who serve as the termination or connection point to those POS POI terminals. Requirements A2.1.2 and A2.1.3 apply to POS POI service providers. The allowance for POS POI terminals that are not currently susceptible to exploits is based on currently known risks. If new exploits are introduced to which POS POI terminals are susceptible, the POS POI terminals will need to be updated immediately. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 343_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A2.1.2** **_Additional requirement for service_**<br>**_providers only:_**All service providers with existing<br>connection points to POS POI terminals that use<br>SSL and/or early TLS as defined in A2.1 have a<br>formal Risk Mitigation and Migration Plan in place<br>that includes:|**A2.1.2** **_Additional testing procedure for service_**<br>**_provider assessments only:_**Review the<br>documented Risk Mitigation and Migration Plan to<br>verify it includes all elements specified in this<br>requirement.|POS POI termination points, including but not<br>limited to service providers such as acquirers or<br>acquirer processors, can continue using SSL/early<br>TLS when it can be shown that the service<br>provider has controls in place that mitigate the risk<br>of supporting those connections for the service<br>provider environment.|
|•<br>Description of usage, including what data is<br>being transmitted, types and number of<br>systems that use and/or support SSL/early<br>TLS, and type of environment.<br>•<br>Risk-assessment results and risk-reduction<br>controls in place.||**Good Practice**<br>Service providers should communicate to all<br>customers using SSL/early TLS about the risks<br>associated with its use and the need to migrate to<br>a secure protocol.<br>**Definitions**|
|•<br>Description of processes to monitor for new<br>vulnerabilities associated with SSL/early TLS.<br>•<br>Description of change control processes that<br>are implemented to ensure SSL/early TLS is<br>not implemented into new environments.||<br>The Risk Mitigation and Migration Plan is a<br>document prepared by the entity that details its<br>plans for migrating to a secure protocol and<br>describes controls the entity has in place to<br>reduce the risk associated with SSL/early TLS|
|•<br>Overview of migration project plan to replace<br>SSL/early TLS at a future date.||until the migration is complete.<br>**Further Information**|
|**Customized Approach Objective**||Refer to the current PCI SSC Information<br>Supplements on SSL/early TLS for further|
|This requirement is not eligible for the customized<br>approach.||guidance on Risk Mitigation and Migration Plans.|
|**Applicability Notes**|||
|This requirement applies only when the entity<br>being assessed is a service provider.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 344_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A2.1.3** **_Additional requirement for service_**<br>**_providers only_**: All service providers provide a<br>secure service offering.<br>**Customized Approach Objective**<br>This requirement is not eligible for the customized<br>approach.|**A2.1.3** **_Additional testing procedure for service_**<br>**_provider assessments only:_**Examine system<br>configurations and supporting documentation to<br>verify the service provider offers a secure protocol<br>option for its service.|Customers must be able to choose to upgrade<br>their POIs to eliminate the vulnerability in using<br>SSL and early TLS. In many cases, customers will<br>need to take a phased or gradual approach to<br>migrate their POS POI estate from the insecure<br>protocol to a secure protocol and so will require<br>the service provider to support a secure offering.<br>**Further Information**<br>Refer to the current PCI SSC Information|
|**Applicability Notes**||Supplements on SSL/Early TLS for further<br>guidance.|
|This requirement applies only when the entity<br>being assessed is a service provider.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 345_ 

#### **_Appendix A3: Designated Entities Supplemental Validation (DESV)_** 

###### **Sections** 

**A3.1** A PCI DSS compliance program is implemented. 

- **A3.2** PCI DSS scope is documented and validated. 

- **A3.3** PCI DSS is incorporated into business-as-usual (BAU) activities. 

- **A3.4** Logical access to the cardholder data environment is controlled and managed. 

- **A3.5** Suspicious events are identified and responded to. 

###### **Overview** 

This Appendix applies only to entities designated by a payment brand(s) or acquirer as requiring additional validation of existing PCI DSS requirements. An entity is required to undergo an assessment according to this Appendix ONLY if instructed to do so by an acquirer or a payment brand. Examples of entities that this Appendix could apply to include: 

- Those storing, processing, and/or transmitting large volumes of account data, 

- Those providing aggregation points for account data, or 

- Those that have suffered significant or repeated breaches of account data. 

Additionally, other PCI standards may reference completion of this Appendix. 

These supplemental validation steps are intended to provide greater assurance that PCI DSS controls are maintained effectively and on a continuous basis through validation of business-as-usual (BAU) processes and increased validation and scoping consideration. 

_(continued on next page)_ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 346_ 

###### _(continued)_ 

**_<mark>Note</mark>_** _<mark>: Some PCI DSS requirements in this Appendix have defined timeframes (for example, an activity that is to be performed at least once every three months or six months). For an initial assessment to such requirements, it is not required that an activity has been performed for</mark> every such timeframe during the previous year, if the assessor verifies:_ 

- _<mark>The activity was performed in accordance with the applicable requirement within the most recent timeframe (for example, the most recent</mark> three-month or six-month period), and_ 

- _The entity has documented policies and procedures for continuing to perform the activity within the defined timeframe._ 

_<mark>For subsequent years after the initial assessment, an activity must have been performed within each required timeframe. For example, an activity required at least every three months must have been performed at least four times during the previous year at an interval that does not</mark> exceed 90-92 days._ 

_<mark>Refer to section 7</mark>_ <mark>Descriptions of Timeframes Used in PCI DSS Requirements</mark> _<mark>for additional guidance about initial assessments.</mark>_ 

Not all requirements in PCI DSS apply to all entities that may undergo a PCI DSS assessment. It is for this reason that some PCI DSS Requirements are duplicated in this appendix. Any questions about this appendix should be addressed to acquirers or payment brands. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 347_ 

###### **Requirements and Testing Procedures Guidance** 

|**A3.1** **A PCI DSS compliance program is implem**|**ented.**||
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**A3.1.1**Responsibility is established by executive<br>management for the protection of account data and<br>a PCI DSS compliance program that includes:<br>•<br>Overall accountability for maintaining PCI DSS<br>compliance.<br>•<br>Defining a charter for a PCI DSS compliance<br>program.<br>•<br>Providing updates to executive management<br>and board of directors on PCI DSS compliance<br>initiatives and issues, including remediation<br>activities, at least once every 12 months.<br>**PCI DSS Reference**:_Requirement 12_<br>**Customized Approach Objective**|**A3.1.1.a**Examine documentation to verify<br>executive management has assigned overall<br>accountability for maintaining the entity’s PCI DSS<br>compliance.<br>**A3.1.1.b**Examine the company’s PCI DSS charter<br>to verify it outlines the conditions under which the<br>PCI DSS compliance program is organized.<br>**A3.1.1.c**Examine executive management and<br>board of directors meeting minutes and/or<br>presentations to ensure PCI DSS compliance<br>initiatives and remediation activities are<br>communicated at least once every 12 months.|Executive management assignment of PCI DSS<br>compliance responsibilities ensures executive-<br>level visibility into the PCI DSS compliance<br>program and allows for the opportunity to ask<br>appropriate questions to determine the<br>effectiveness of the program and influence<br>strategic priorities.<br>**Good Practice**<br>Executive management may include C-level<br>positions, board of directors, or equivalent. The<br>specific titles will depend on the particular<br>organizational structure.<br>Responsibility for the PCI DSS compliance<br>program may be assigned to individual roles<br>and/or to business units within the organization.|
|This requirement is not eligible for the customized<br>approach|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 348_ 

|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**A3.1.2**A formal PCI DSS compliance program is in<br>place that includes:<br>•<br>Definition of activities for maintaining and<br>monitoring overall PCI DSS compliance,<br>|**A3.1.2.a**Examine information security policies and<br>procedures to verify that processes are defined for<br>a formal PCI DSS compliance program that<br>includes all elements specified in this requirement.|A formal compliance program allows an<br>organization to monitor the health of its security<br>controls, be proactive if a control fails, and<br>effectively communicate activities and compliance<br>status throughout the organization.|
|including business-as-usual activities.<br>•<br>Annual PCI DSS assessment processes.<br>•<br>Processes for the continuous validation of PCI<br>DSS requirements (for example, daily, weekly,<br>every three months, as applicable per the<br>requirement).|**A3.1.2.b**Interview personnel and observe<br>compliance activities to verify that a formal PCI<br>DSS compliance program is implemented in<br>accordance with all elements specified in this<br>requirement.|**Good Practice**<br>The PCI DSS compliance program can be a<br>dedicated program or part of overarching<br>compliance and/or governance program, and<br>should include a well-defined methodology that<br>demonstrates consistent and effective evaluation.|
|•<br>A process for performing business-impact<br>analysis to determine potential PCI DSS impacts<br>for strategic business decisions.<br>**PCI DSS Reference**:_Requirements 1-12_||Strategic business decisions that should be<br>analyzed for potential PCI DSS impacts may<br>include mergers and acquisitions, new technology<br>purchases, or new payment-acceptance<br>channels.|
|**Customized Approach Objective**||**Definitions**|
|This requirement is not eligible for the customized<br>approach.||Maintaining and monitoring an organization’s<br>overall PCI DSS compliance includes identifying<br>activities to be performed daily, weekly, monthly,<br>every three months, or annually, and ensuring<br>these activities are being performed accordingly<br>(for example, using a security self-assessment or<br>PDCA methodology).<br>**Examples**<br>Methodologies that support the management of<br>compliance programs include Plan-Do-Check-Act<br>(PDCA), ISO 27001, COBIT, DMAIC, and Six<br>Sigma.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 349_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A3.1.3**PCI DSS compliance roles and<br>responsibilities are specifically defined and formally<br>assigned to one or more personnel, including:<br>•<br>Managing PCI DSS business-as-usual activities.<br>•<br>Managing annual PCI DSS assessments.<br>•<br>Managing continuous validation of PCI DSS|**A3.1.3.a**Examine information security policies and<br>procedures and interview personnel to verify that<br>PCI DSS compliance roles and responsibilities are<br>specifically defined and formally assigned to one or<br>more personnel in accordance with all elements of<br>this requirement.|The formal definition of specific PCI DSS<br>compliance roles and responsibilities helps to<br>ensure accountability and monitoring of ongoing<br>PCI DSS compliance efforts.<br>**Good Practice**<br>Ownership should be assigned to individuals with<br>the authority to make risk-based decisions, and|
|requirements (for example, daily, weekly, every<br>three months, as applicable per the<br>requirement).<br>•<br>Managing business-impact analysis to<br>determine potential PCI DSS impacts for<br>strategic business decisions.<br>**PCI DSS Reference**:_Requirement 12_|**A3.1.3.b**Interview responsible personnel and<br>verify they are familiar with and performing their<br>designated PCI DSS compliance responsibilities.|upon whom accountability rests for the specific<br>function. Duties should be formally defined, and<br>owners should be able to demonstrate an<br>understanding of their responsibilities and<br>accountability.<br>Compliance roles may be assigned to a single<br>owner or multiple owners for different requirement<br>elements.|
|**Customized Approach Objective**|||
|This requirement is not eligible for the customized<br>approach.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 350_ 

|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**A3.1.4**Up-to-date PCI DSS and/or information<br>security training is provided at least once every 12<br>months to personnel with PCI DSS compliance<br>responsibilities (as identified in A3.1.3).<br>**PCI DSS Reference**:_Requirement 12_|**A3.1.4.a**Examine information security policies and<br>procedures to verify that PCI DSS and/or<br>information security training is required at least<br>once every 12 months for each role with PCI DSS<br>compliance responsibilities.|Personnel responsible for PCI DSS compliance<br>have specific training needs exceeding that which<br>is typically provided by general security<br>awareness training to enable them to perform<br>their role.<br>**Good Practice**|
||**A3.1.4.b**Interview personnel and examine<br>certificates of attendance or other records to verify|Individuals with PCI DSS compliance<br>responsibilities should receive specialized training|
|**Customized Approach Objective**|<br>that personnel with PCI DSS compliance<br>responsibility receive up-to-date PCI DSS and/or|that, in addition to a general awareness of<br>information security, focuses on specific security|
|This requirement is not eligible for the customized<br>approach.|<br>similar information security training at least once<br>every 12 months.|topics, skills, processes, or methodologies that<br>must be followed for those individuals to perform<br>their compliance responsibilities effectively.<br>Training may be offered by third parties such as<br>the PCI SSC (for example, PCI Awareness, PCIP,<br>and ISA), payment brands, and acquirers, or<br>training may be internal. Training content should<br>be applicable for the individual’s job function, be<br>current, and include the latest security threats<br>and/or version of PCI DSS.<br>**Further Information**<br>For additional guidance, refer to_Information_<br>_Supplement: Best Practices for Implementing a_<br>_Security Awareness Program_.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 351_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**A3.2** **PCI DSS scope is documented and validate**<br>|**d.**<br>||
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**A3.2.1**PCI DSS scope is documented and<br>confirmed for accuracy at least once every three<br>months and upon significant changes to the in-<br>scope environment. At a minimum, the scoping<br>validation includes:<br>•<br>Identifying all data flows for the various payment<br>stages (for example, authorization, capture,<br>settlement, chargebacks, and refunds) and<br>acceptance channels (for example, card-<br>present, card-not-present, and e-commerce).|**A3.2.1.a**Examine documented results of scope<br>reviews and interview personnel to verify that the<br>reviews are performed:<br>•<br>At least once every three months.<br>•<br>After significant changes to the in-scope<br>environment.|Frequent validation of PCI DSS scope helps to<br>ensure PCI DSS scope remains up to date and<br>aligned with changing business objectives, and<br>therefore that security controls are protecting all<br>appropriate system components.<br>**Good Practice**<br>Accurate scoping involves critically evaluating the<br>CDE and all connected system components to<br>determine the necessary coverage for PCI DSS<br>requirements. Scoping activities, including careful<br>analysis and ongoing monitoring, help to ensure|
|•<br>Updating all data-flow diagrams per<br>Requirement 1.2.4.<br>•<br>Identifying all locations where account data is<br>stored, processed, and transmitted, including but<br>not limited to 1) any locations outside of the<br>currently defined CDE, 2) applications that<br>process CHD, 3) transmissions between<br>systems and networks, and 4) file backups.|**A3.2.1.b**Examine documented results of scope<br>reviews occurring at least once every three months<br>to verify that scoping validation includes all<br>elements specified in this requirement.|<br>that in-scope systems are appropriately secured.<br>When documenting account data locations, the<br>entity can consider creating a table or<br>spreadsheet that includes the following<br>information:<br>•<br>Data stores (databases, files, cloud, etc.),<br>including purpose of data storage and the<br>retention period,|
|•<br>For any account data found outside of the<br>currently defined CDE, either 1) securely delete<br>it, 2) migrate it into the currently defined CDE, or<br>3) expand the currently defined CDE to include<br>it.<br>•<br>Identifying all system components in the CDE,<br>connected to the CDE, or that could impact<br>security of the CDE.<br>_(continued on next page)_||•<br>Which CHD elements are stored (PAN, expiry<br>date, cardholder name, and/or any elements<br>of SAD prior to completion of authorization),<br>•<br>How data is secured (type of encryption and<br>strength, hashing algorithm and strength,<br>truncation, tokenization),<br>•<br>How access to data stores is logged, including<br>a description of logging mechanism(s) in use<br>(enterprise solution, application level,<br>operating system level, etc.).<br>_(continued on next page)_|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 352_ 

|**Requirements and Testing Procedures**|**Guidance**|
|---|---|
|•<br>Identifying all segmentation controls in use and<br>the environment(s) from which the CDE is<br>segmented, including justification for<br>environments being out of scope<br>•<br>Identifying all connections to third-party entities<br>with access to the CDE.<br>•<br>Confirming that all identified data flows, account<br>data, system components, segmentation<br>controls, and connections from third parties with<br>access to the CDE are included in scope.<br>**PCI DSS Reference**:_Scope of PCI DSS_<br>_Requirements, Requirement 12._|In addition to internal systems and networks, all<br>connections from third-party entities—for<br>example, business partners, entities providing<br>remote support services, and other service<br>providers—need to be identified to determine<br>inclusion for PCI DSS scope. Once the in-scope<br>connections have been identified, the applicable<br>PCI DSS controls can be implemented to reduce<br>the risk of a third-party connection being used to<br>compromise an entity’s CDE.<br>A data discovery tool or methodology can be used<br>to facilitate identifying all sources and locations of<br>PAN, and to look for PAN that resides on systems<br>and networks outside the currently defined CDE|
|**Customized Approach Objective**<br>This requirement is not eligible for the customized<br>approach.|or in unexpected places within the defined CDE—<br>for example, in an error log or memory dump file.<br>This approach can help ensure that previously<br>unknown locations of PAN are detected and that<br>the PAN is either eliminated or properly secured.<br>**Further Information**<br>Refer to_Information Supplement: Guidance for_<br>_PCI DSS Scoping and Network Segmentation_for<br>additional guidance.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 353_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A3.2.2**PCI DSS scope impact for all changes to<br>systems or networks is determined, including<br>additions of new systems and new network<br>connections. Processes include:<br>•<br>Performing a formal PCI DSS impact<br>assessment.|**A3.2.2**Examine change documentation and<br>interview personnel to verify that for each change<br>to systems or networks the PCI DSS scope impact<br>is determined, and includes all elements specified<br>in this requirement.|Changes to systems or networks can have a<br>significant impact on PCI DSS scope. For<br>example, changes to network security control<br>rulesets can bring whole network segments into<br>scope, or new systems may be added to the CDE<br>that have to be appropriately protected.<br>A formal impact assessment performed in|
|•<br>Identifying applicable PCI DSS requirements to<br>the system or network.<br>•<br>Updating PCI DSS scope as appropriate.<br>•<br>Documented sign-off of the results of the impact||advance of a change gives the entity assurance<br>that the change will not adversely affect the<br>security of the CDE.<br>**Good Practice**|
|assessment by responsible personnel (as<br>defined in A3.1.3).||Processes to determine the potential impact that<br>changes to systems and networks may have on|
|**PCI DSS Reference**:_Scope of PCI DSS_<br>_Requirements; Requirements 1-12_||an entity’s PCI DSS scope may be performed as<br>part of a dedicated PCI DSS compliance program<br>or may fall under an entity’s overarching|
|**Customized Approach Objective**||compliance and/or governance program.|
|This requirement is not eligible for the customized<br>approach.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 354_ 

###### **Guidance** 

|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**A3.2.2.1**Upon completion of a change, all relevant<br>PCI DSS requirements are confirmed to be<br>implemented on all new or changed systems and<br>networks, and documentation is updated as<br>applicable.<br>**PCI DSS Reference**:_Scope of PCI DSS_<br>_Requirements; Requirement 1-12_|**A3.2.2.1**Examine change records and the affected<br>systems/networks, and interview personnel to<br>verify that all relevant PCI DSS requirements were<br>confirmed to be implemented and documentation<br>updated as part of the change.|It is important to have processes to analyze all<br>changes made to systems or networks, to ensure<br>that all appropriate PCI DSS controls are applied<br>to any systems or networks added to the in-scope<br>environment due to a change.<br>Building this validation into change management<br>processes helps ensure that device inventories<br>and configuration standards are kept up to date,<br>|
|**Customized Approach Objective**||and security controls are applied where needed.<br>**Good Practice**|
|This requirement is not eligible for the customized<br>approach.||A change management process should include<br>supporting evidence that PCI DSS requirements<br>are implemented or preserved through an iterative<br>process.<br>**Examples**<br>PCI DSS requirements that should be verified<br>include, but are not limited to:<br>•<br>Network diagrams are updated to reflect<br>changes.<br>•<br>Systems are configured per configuration<br>standards, with all default passwords changed<br>and unnecessary services disabled.<br>•<br>Systems are protected with required<br>controls—for example, file integrity monitoring,<br>antimalware, patches, and audit logging.<br>•<br>Sensitive authentication data is not stored,<br>and all account data storage is documented<br>and incorporated into data-retention policy and<br>procedures.<br>•<br>New systems are included in the quarterly<br>vulnerability scanning process.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 355_ 

|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**A3.2.3**Changes to organizational structure result in<br>a formal (internal) review of the impact to PCI DSS<br>scope and applicability of controls.<br>**PCI DSS Reference**:_Requirement 12_<br>**Customized Approach Objective**<br>This requirement is not eligible for the customized<br>approach.|**A3.2.3**Examine policies and procedures to verify<br>that a change to organizational structure results in<br>formal a review of the impact on PCI DSS scope<br>and applicability of controls.|An organization’s structure and management<br>define the requirements and protocol for effective<br>and secure operations. Changes to this structure<br>could have negative effects to existing controls<br>and frameworks by reallocating or removing<br>resources that once supported PCI DSS controls<br>or inheriting new responsibilities that may not<br>have established controls in place. Therefore, it is<br>important to revisit PCI DSS scope and controls<br>when there are changes to an organization’s<br>structure and management to ensure controls are<br>in place and active.<br>**Examples**<br>Changes to organizational structure include, but<br>are not limited to, company mergers or<br>acquisitions, and significant changes or<br>reassignments of personnel with responsibility for<br>security control.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 356_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A3.2.4**If segmentation is used, PCI DSS scope is<br>confirmed as follows:<br>•<br>Per the entity’s methodology defined at<br>Requirement 11.4.1.<br>•<br>Penetration testing is performed on<br>segmentation controls at least once every six<br>months and after any changes to segmentation<br>controls/methods.|**A3.2.4**Examine the results from the most recent<br>penetration test to verify that the test was<br>conducted in accordance with all elements<br>specified in this requirement.|PCI DSS normally requires segmentation controls<br>to be verified by penetration testing every twelve<br>months.<br>Validating segmentation controls more frequently<br>is likely to discover failings in segmentation before<br>they can be exploited by an attacker attempting to<br>pivot laterally from an out-of-scope untrusted<br>network to the CDE.<br>**Good Practice**|
|•<br>The penetration testing covers all segmentation<br>controls/methods in use.<br>•<br>The penetration testing verifies that<br>segmentation controls/methods are operational<br>and effective, and isolate the CDE from all out-<br>of-scope systems.||Although the requirement specifies that this scope<br>validation is carried out at least once every six<br>months and after a significant change, this<br>exercise should be performed as frequently as<br>possible to ensure it remains effective at isolating<br>the CDE from other networks.|
|**PCI DSS Reference**:_Requirement 11_||**Further Information**|
|**Customized Approach Objective**||Refer to_Information Supplement: Penetration_<br>_Testing Guidance_for additional guidance.|
|This requirement is not eligible for the customized<br>approach.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 357_ 

|**Requirements and**|**Testing Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**A3.2.5**A data-discovery methodology is<br>implemented that:<br>•<br>Confirms PCI DSS scope.|**A3.2.5.a**Examine the documented data-discovery<br>methodology to verify it includes all elements<br>specified in this requirement.|PCI DSS requires that, as part of the scoping<br>exercise, assessed entities must identify and<br>document the existence of all cleartext PAN in<br>their environments. Implementing a data-|
|•<br>Locates all sources and locations of cleartext<br>PAN at least once every three months and<br>upon significant changes to the CDE or<br>processes.<br>•<br>Addresses the potential for cleartext PAN to<br>reside on systems and networks outside the<br>currently defined CDE.|**A3.2.5.b**Examine results from recent data<br>discovery efforts, and interview responsible<br>personnel to verify that data discovery is performed<br>at least once every three months and upon<br>significant changes to the CDE or processes.|discovery methodology that identifies all sources<br>and locations of cleartext PAN and looks for<br>cleartext PAN on systems and networks outside<br>the currently defined CDE or in unexpected<br>places within the defined CDE—for example, in<br>an error log or memory dump file— helps to<br>ensure that previously unknown locations of<br>cleartext PAN are detected and properly secured.|
|**PCI DSS Reference**:_Scope of PCI DSS_<br>_Requirements_||**Examples**<br>A data-discovery process can be performed via a|
|**Customized Approach Objective**||variety of methods, including, but not limited to 1)<br>commercially available data-discovery software,|
|This requirement is not eligible for the customized<br>approach||2) an in-house developed data-discovery<br>program, or 3) a manual search. A combination of<br>methodologies may also be used as needed.<br>Regardless of the method used, the goal of the<br>effort is to find all sources and locations of<br>cleartext PAN (not just in the defined CDE).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 358_ 

|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**A3.2.5.1**Data discovery methods are confirmed as<br>follows:|**A3.2.5.1.a**Interview personnel and review<br>documentation to verify:|A process to test the effectiveness of the methods<br>used for data discovery ensures the<br>completeness and accuracy of account data|
|•<br>Effectiveness of methods is tested.<br>•<br>Methods are able to discover cleartext PAN on<br>all types of system components and file formats<br>in use.<br>•<br>The effectiveness of data-discovery methods is<br>confirmed at least once every 12 months.|•<br>The entity has a process in place to test the<br>effectiveness of methods used for data<br>discovery.<br>•<br>The process includes verifying the methods are<br>able to discover cleartext PAN on all types of<br>system components and file formats in use.|detection.<br>**Good Practice**<br>For completeness, system components in the in-<br>scope networks, and systems in out-of-scope<br>networks, should be included in the data-<br>discovery process.|
|**PCI DSS Reference**:_Scope of PCI DSS_<br>_Requirements_|**A3.2.5.1.b**Examine the results of effectiveness<br>tests to verify that the effectiveness of data-|The data-discovery process should be effective<br>on all operating systems and platforms in use.<br>Accuracy can be tested by placing test PANs on|
|**Customized Approach Objective**|discovery methods is confirmed at least once every<br>12 months.|<br>system components and file formats in use and<br>confirming that the data-discovery method|
|This requirement is not eligible for the customized<br>approach.||detected the test PANs.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 359_ 

|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**A3.2.5.2**Response procedures are implemented to<br>be initiated upon the detection of cleartext PAN<br>outside the CDE to include:<br>•<br>Determining what to do if cleartext PAN is<br>discovered outside the CDE, including its<br>til  dlti d/ iti it|**A3.2.5.2.a**Examine documented response<br>procedures to verify that procedures for responding<br>to the detection of cleartext PAN outside the CDE<br>are defined and include all elements specified in<br>this requirement.|Having documented response procedures that are<br>followed in the event cleartext PAN is found<br>outside the CDE helps to identify the necessary<br>remediation actions and prevent future leaks.<br>**Good Practice**<br>If PAN was found outside the CDE, an analysis|
|rereva, secure eeon, anor mgraon no<br>the currently defined CDE, as applicable.<br>•<br>Determining how the data ended up outside the<br>CDE.<br>•<br>Remediating data leaks or process gaps that<br>resulted in the data being outside the CDE.<br>•<br>Identifying the source of the data.<br>•<br>Identifying whether any track data is stored with<br>the PANs.|**A3.2.5.2.b**Interview personnel and examine<br>records of response actions to verify that<br>remediation activities are performed when cleartext<br>PAN is detected outside the CDE.|should be performed to 1) determine whether it<br>was saved independently of other data or with<br>sensitive authentication data, 2) to identify the<br>source of the data, and 3) identify the control gaps<br>that resulted in the data being outside the CDE.<br>Entities should consider whether contributory<br>factors, such as business processes, user<br>behavior, improper system configurations, etc.,<br>caused the PAN to be stored in an unexpected<br>location. If such contributory factors are present,|
|**Customized Approach Objective**||they should be addressed per this Requirement to<br>prevent a recurrence.|
|This requirement is not eligible for the customized<br>approach.|||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 360_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A3.2.6**Mechanisms are implemented for detecting<br>and preventing cleartext PAN from leaving the CDE<br>via an unauthorized channel, method, or process,<br>including mechanisms that are:<br>|**A3.2.6.a**Examine documentation and observe<br>implemented mechanisms to verify that the<br>mechanisms are in accordance with all elements<br>specified in this requirement.|The use of mechanisms to detect and prevent<br>unauthorized PAN from leaving the CDE allows<br>an organization to detect and prevent situations<br>that may lead to data loss.<br>**Good Practice**|
|•<br>Actively running.<br>•<br>Configured to detect and prevent cleartext PAN<br>leaving the CDE via an unauthorized channel,<br>method, or process.<br>•<br>Generating audit logs and alerts upon detection<br>of cleartext PAN leaving the CDE via an<br>unauthorized channel, method, or process.<br>**PCI DSS Reference**:_Scope of PCI DSS_<br>_Requirements, Requirement 12_|**A3.2.6.b**Examine audit logs and alerts, and<br>interview responsible personnel to verify that alerts<br>are investigated.|Coverage of the mechanisms should include, but<br>not be limited to, e-mails, downloads to removable<br>media, and output to printers.<br>**Examples**<br>Mechanisms to detect and prevent unauthorized<br>loss of cleartext PAN may include the use of<br>appropriate tools such as data loss prevention<br>(DLP) solutions as well as manual processes and<br>procedures.|



- Generating audit logs and alerts upon detection of cleartext PAN leaving the CDE via an unauthorized channel, method, or process. 

- **PCI DSS Reference** : _Scope of PCI DSS Requirements, Requirement 12_ **Customized Approach Objective** This requirement is not eligible for the customized approach. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 361_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A3.2.6.1**Response procedures are implemented to<br>be initiated upon the detection of attempts to<br>remove cleartext PAN from the CDE via an<br>unauthorized channel, method, or process.<br>Response procedures include:<br>•<br>Procedures for the prompt investigation of alerts<br>by responsible personnel.<br>•<br>Procedures for remediating data leaks or<br>process gaps, as necessary, to prevent any data<br>loss.|**A3.2.6.1.a**Examine documented response<br>procedures to verify that procedures for responding<br>to the attempted removal of cleartext PAN from the<br>CDE via an unauthorized channel, method, or<br>process include all elements specified in this<br>requirement:<br>•<br>Procedures for the prompt investigation of<br>alerts by responsible personnel.<br>•<br>Procedures for remediating data leaks or<br>process gaps, as necessary, to prevent any|Attempts to remove cleartext PAN via an<br>unauthorized channel, method, or process may<br>indicate malicious intent to steal data, or may be<br>the actions of an authorized employee who is<br>unaware of or simply not following the proper<br>methods. Prompt investigation of these<br>occurrences can identify where remediation<br>needs to be applied and provides valuable<br>information to help understand from where the<br>threats are coming.|
|**PCI DSS Reference**:_Requirement 12_|data loss.||
|**Customized Approach Objective**|**A3.2.6.1.b**Interview personnel and examine<br>records of actions taken when cleartext PAN is<br>detected leaving the CDE via an unauthorized<br>channel, method, or process and verify that||
|This requirement is not eligible for the customized<br>approach.|remediation activities were performed.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 362_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **A3.3 PCI DSS is incorporated into business-as-usual (BAU) activities.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A3.3.1**Failures of critical security control systems<br>are detected, alerted, and addressed promptly,<br>including but not limited to failure of:<br>•<br>Network security controls<br>•<br>IDS/IPS|**A3.3.1.a**Examine documented policies and<br>procedures to verify that processes are defined to<br>promptly detect, alert, and address critical security<br>control failures in accordance with all elements<br>specified in this requirement.|Without formal processes for the prompt (as soon<br>as possible) detection, alerting, and addressing of<br>critical security control failures, failures may go<br>undetected or remain unresolved for extended<br>periods. In addition, without formalized time-<br>bound processes, attackers will have ample time<br>|
|•<br>FIM|**A3.3.1.b**Examine detection and alerting|to compromise systems and steal account data<br>from the CDE.|
|•<br>Anti-malware solutions<br>•<br>Physical access controls<br>•<br>Logical access controls<br>|processes, and interview personnel to verify that<br>processes are implemented for all critical security<br>controls specified in this requirement and that each<br>failure of a critical security control results in the|**Good Practice**<br>The specific types of failures may vary, depending<br>on the function of the device system component<br>|
|•<br>Audit logging mechanisms|generation of an alert.|and technology in use. Typical failures include a<br>|
|•<br>Segmentation controls (if used)<br>•<br>Automated audit log review mechanisms._This_<br>||system ceasing to perform its security function or<br>not functioning in its intended manner, such as a<br>firewall erasing all its rules or going offline.|



- Automated audit log review mechanisms. _This bullet is a best practice until its effective date; refer to Applicability Notes below for details._ 

- Automated code review tools (if used). _This bullet is a best practice until its effective date; refer to Applicability Notes below for details._ 

- **PCI DSS Reference** : _Requirements 1-12_ 

**Customized Approach Objective** This requirement is not eligible for the customized approach. _(continued on next page)_ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 363_ 

|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Applicability Notes**|||
|_The bullets above (for automated log review_<br>_mechanisms and automated code review tools (if_<br>_used)) are best practices until 31 March 2025, after_<br>_which they will be required as part of Requirement_<br>_A3.3.1 and must be fully considered during a PCI_<br>_DSS assessment._|||
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**A3.3.1.1**Failures of any critical security control<br>systems are responded to promptly. Processes for<br>responding to failures in security control systems<br>include:<br>•<br>Restoring security functions.<br>•<br>Identifying and documenting the duration (date<br>|**A3.3.1.1.a**Examine documented policies and<br>procedures and interview personnel to verify<br>processes are defined and implemented to<br>respond promptly to a security control failure in<br>accordance with all elements specified in this<br>requirement.|If alerts from failures of critical security control<br>systems are not responded to quickly and<br>effectively, attackers may use this time to insert<br>malicious software, gain control of a system, or<br>steal data from the entity’s environment.<br>**Good Practice**<br>Documented evidence (for example, records|
|and time from start to end) of the security failure.<br>•<br>Identifying and documenting the cause(s) of<br>failure, including root cause, and documenting<br>remediation required to address the root cause.<br>•<br>Identifying and addressing any security issues<br>that arose during the failure.<br>|**A3.3.1.1.b**Examine records to verify that security<br>control failures are documented to include:<br>•<br>Identification of cause(s) of the failure,<br>including root cause.<br>•<br>Duration (date and time start and end) of the<br>security failure.|within a problem management system) should<br>support processes and procedures in place that<br>respond to security failures. In addition, personnel<br>should be aware of their responsibilities in the<br>event of a failure. Actions and responses to the<br>failure should be captured in the documented<br>evidence.|



- Determining whether further actions are required as a result of the security failure. 

   - Details of the remediation required to address the root cause. 

- Implementing controls to prevent the cause of failure from reoccurring. 

- Resuming monitoring of security controls. 

- **PCI DSS Reference** : _Requirements 1-12_ 

###### **Customized Approach Objective** 

This requirement is not eligible for the customized approach. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 364_ 

###### **Requirements and Testing Procedures Guidance** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A3.3.2**Hardware and software technologies are<br>reviewed at least once every 12 months to confirm<br>whether they continue to meet the organization’s<br>PCI DSS requirements.<br>**PCI DSS Reference**:_Requirements 2, 6, 12._|**A3.3.2.a**Examine documented policies and<br>procedures and interview personnel to verify<br>processes are defined and implemented to review<br>hardware and software technologies to confirm<br>whether they continue to meet the organization’s<br>PCI DSS requirements.|Hardware and software technologies are<br>constantly evolving, and organizations need to be<br>aware of changes to the technologies they use, as<br>well as the evolving threats to those technologies.<br>Conducting appropriate reviews of these<br>technologies ensures that they can prepare for,<br>and manage, vulnerabilities in hardware and|
||**A3.3.2.b**Review the results of the recent reviews<br>of hardware and software technologies to verify<br>reviews are performed at least once every 12<br>months.|software that will not be remediated by the vendor<br>or developer.<br>**Good Practice**<br>Organizations should also consider reviewing<br>firmware versions to ensure they remain current|
||**A3.3.2.c**Review documentation to verify that, for|and supported by the vendors.|
||any technologies that have been determined to no|Organizations also need to be aware of changes|
|**Customized Approach Objective**<br>This requirement is not eligible for the customized|longer meet the organization’s PCI DSS<br>requirements, a plan is in place to remediate the<br>technology.|made by technology vendors to their products or<br>processes to understand how such changes may<br>impact the organization’s use of the technology.|
|approach.||Regular reviews of technologies that impact or<br>influence PCI DSS controls can assist with|
|**Applicability Notes**||purchasing, usage, and deployment strategies<br>and ensure controls that rely on those|
|The process includes a plan for remediating<br>technologies that no longer meet the organization’s<br>PCI DSS requirements, up to and including<br>replacement of the technology, as appropriate.||technologies remain effective. These reviews<br>include, but are not limited to, reviewing<br>technologies that are no longer supported by the<br>vendor and/or no longer meet the security needs<br>of the organization.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 365_ 

|**Requirements and T**|**esting Procedures**|**Guidance**|
|---|---|---|
|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|**A3.3.3**Reviews are performed at least once every<br>three months to verify BAU activities are being<br>followed. Reviews are performed by personnel<br>assigned to the PCI DSS compliance program (as<br>identified in A3.1.3), and include:<br>•<br>Confirmation that all BAU activities, including<br>A3.2.2, A3.2.6, and A3.3.1, are being performed.|**A3.3.3.a**Examine policies and procedures to verify<br>that processes are defined for reviewing and<br>verifying BAU activities in accordance with all<br>elements specified in this requirement.|Regularly confirming that security policies and<br>procedures are being followed provides<br>assurance that the expected controls are active<br>and working as intended. The objective of these<br>reviews is not to reperform other PCI DSS<br>requirements, but to confirm that security activities<br>are being performed on an ongoing basis.<br>**Good Practice**|
|•<br>Confirmation that personnel are following<br>||These reviews can also be used to verify that|
|security policies and operational procedures (for<br>example, daily log reviews, ruleset reviews for<br>network security controls, configuration<br>standards for new systems).<br>•<br>Documenting how the reviews were completed,<br>including how all BAU activities were verified as<br>being in place.<br>•<br>Collection of documented evidence as required<br>for the annual PCI DSS assessment.<br>•<br>Review and sign-off of results by personnel<br>assigned responsibility for the PCI DSS<br>compliance program, as identified in A3.1.3.<br>•<br>Retention of records and documentation for at<br>least 12 months, covering all BAU activities.<br>**PCI DSS Reference**:_Requirements 1-12_|**A3.3.3.b**Interview responsible personnel and<br>examine records of reviews to verify that:<br>•<br>Reviews are performed by personnel assigned<br>to the PCI DSS compliance program.<br>•<br>Reviews are performed at least once every<br>three months.|<br>appropriate evidence is being maintained—for<br>example, audit logs, vulnerability scan reports,<br>reviews of network security control rulesets—to<br>assist in the entity’s preparation for its next PCI<br>DSS assessment.<br>**Examples**<br>Looking at Requirement 1.2.7 as one example,<br>Requirement A3.3.3 is met by confirming, at least<br>once every three months, that reviews of<br>configurations of network security controls have<br>occurred at the required frequency. On the other<br>hand, Requirement 1.2.7 is met by reviewing<br>those configurations as specified in the<br>requirement.|



|**Customized Approach Objective**|
|---|
|This requirement is not eligible for the customized<br>approach.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 366_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

**A3.4 Logical access to the cardholder data environment is controlled and managed.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A3.4.1**User accounts and access privileges to in-<br>scope system components are reviewed at least<br>once every six months to ensure user accounts and<br>access privileges remain appropriate based on job<br>function, and that all access is authorized.<br>**PCI DSS Reference**:_Requirement 7_<br>**Customized Approach Objective**<br>This requirement is not eligible for the customized<br>approach.|**A3.4.1**Interview responsible personnel and<br>examine supporting documentation to verify that:<br>•<br>User accounts and access privileges are<br>reviewed at least every six months.<br>•<br>Reviews confirm that access is appropriate<br>based on job function and that all access is<br>authorized.|Regular review of access rights helps to detect<br>excessive access rights remaining after user job<br>responsibilities change, system functions change,<br>or other modifications. If excessive user rights are<br>not revoked in due time, they may be used by<br>malicious users for unauthorized access.<br>This review provides another opportunity to<br>ensure that accounts for all terminated users have<br>been removed (if any were missed at the time of<br>termination), as well as to ensure that any third<br>parties that no longer need access have had their<br>access terminated.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 367_ 

###### **Requirements and Testing Procedures** 

###### **Guidance** 

###### **A3.5 Suspicious events are identified and responded to.** 

|**Defined Approach Requirements**|**Defined Approach Testing Procedures**|**Purpose**|
|---|---|---|
|**A3.5.1**A methodology is implemented for the<br>prompt identification of attack patterns and<br>undesirable behavior across systems that includes:<br>•<br>Identification of anomalies or suspicious activity<br>as it occurs.<br>•<br>Issuance of prompt alerts upon detection of|**A3.5.1.a**Examine documentation and interview<br>personnel to verify a methodology is defined and<br>implemented to identify attack patterns and<br>undesirable behavior across systems in a prompt<br>manner, and includes all elements specified in this<br>requirement.|The ability to identify attack patterns and<br>undesirable behavior across systems—for<br>example, using centrally managed or automated<br>log-correlation tools— is critical in preventing,<br>detecting, or minimizing the impact of a data<br>compromise. The presence of logs in all<br>environments allows thorough tracking, alerting,<br>|
|suspicious activity or anomaly to responsible<br>personnel.<br>•<br>Response to alerts in accordance with<br>documented response procedures.<br>**PCI DSS Reference**:_Requirements 10, 12_<br>**Customized Approach Objective**<br>This requirement is not eligible for the customized<br>approach.|**A3.5.1.b**Examine incident response procedures<br>and interview responsible personnel to verify that:<br>•<br>On-call personnel receive prompt alerts.<br>•<br>Alerts are responded to per documented<br>response procedures.|and analysis when something goes wrong.<br>Determining the cause of a compromise is very<br>difficult, if not impossible, without a process to<br>corroborate information from critical system<br>components and systems that perform security<br>functions, such as network security controls,<br>IDS/IPS, and file integrity monitoring (FIM)<br>systems. Thus, logs for all critical system<br>components and systems that perform security<br>functions need to be collected, correlated, and<br>maintained. This could include using software<br>products and service methodologies to provide<br>real-time analysis, alerting, and reporting, such as<br>security information and event management<br>(SIEM), FIM, or change detection.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 368_ 

## **Appendix B Compensating Controls** 

Compensating controls may be considered when an entity cannot meet a PCI DSS requirement explicitly as stated, due to legitimate and documented technical or business constraints but has sufficiently mitigated the risk associated with not meeting the requirement through implementation of other, or compensating, controls. 

Compensating controls must satisfy the following criteria: 

1. Meet the intent and rigor of the original PCI DSS requirement. 

2. Provide a similar level of defense as the original PCI DSS requirement, such that the compensating control sufficiently offsets the risk that the original PCI DSS requirement was designed to defend against. To understand the intent of a requirement, see _the Customized Approach Objective_ for most PCI DSS requirements. If a requirement is not eligible for the Customized Approach and therefore does not have a Customized Approach Objective, refer to the **Purpose** in the Guidance column for that requirement. 

3. Be “above and beyond” other PCI DSS requirements. (Simply being in compliance with other PCI DSS requirements is not a compensating control.) 

4. When evaluating “above and beyond” for compensating controls, consider the following: 

   - a) Existing PCI DSS requirements CANNOT be considered as compensating controls if they are already required for the item under review. For example, passwords for non-console administrative access must be sent encrypted to mitigate the risk of intercepting cleartext administrative passwords. An entity **_Note:_** _All compensating controls_ cannot use other PCI DSS password requirements (intruder lockout, complex passwords, _must be reviewed and validated for_ etc.) to compensate for lack of encrypted passwords, since those other password _sufficiency by the assessor who_ requirements do not mitigate the risk of interception of cleartext passwords. Also, the other _conducts the PCI DSS_ password controls are already PCI DSS requirements for the item under review _assessment. The effectiveness of_ (passwords). _a compensating control is_ 

**_Note:_** _All compensating controls must be reviewed and validated for sufficiency by the assessor who conducts the PCI DSS assessment. The effectiveness of a compensating control is dependent on the specifics of the environment in which the control is implemented, the surrounding security controls, and the configuration of the control. Entities should be aware that a given compensating control will not be effective in all environments._ 

- b) Existing PCI DSS requirements MAY be considered as compensating controls if they are required for another area but are not required for the item under review. 

- c) Existing PCI DSS requirements may be combined with new controls to become a compensating control. For example, if a company is unable to address a vulnerability that is exploitable through a network interface because a security update is not yet available from a vendor, a compensating control could consist of controls that include all of the following: 1) internal network segmentation, 2) limiting network access to the vulnerable interface to only required devices (IP address or MAC address filtering), and 3) IDS/IPS monitoring of all traffic destined to the vulnerable interface. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 369_ 

5. Address the additional risk imposed by not adhering to the PCI DSS requirement. 

6. Address the requirement currently and in the future. A compensating control cannot address a requirement that was missed in the past (for example, where performance of a task was required two quarters ago, but that task was not performed). 

The assessor is required to thoroughly evaluate compensating controls during each annual PCI DSS assessment to confirm that each compensating control adequately addresses the risk that the original PCI DSS requirement was designed to address, per items 1-6 above. 

To maintain compliance, processes and controls must be in place to ensure compensating controls remain effective after the assessment is complete. Additionally, compensating control results must be documented in the applicable report for the assessment (for example, a Report on Compliance or a Self-Assessment Questionnaire) in the corresponding PCI DSS requirement section, and included when the applicable report is submitted to the requesting organization. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 370_ 

## **Appendix C Compensating Controls Worksheet** 

The entity must use this worksheet to define compensating controls for any requirement where compensating controls are used to meet a PCI DSS requirement. Note that compensating controls should also be documented in accordance with instructions in the Report on Compliance in the corresponding PCI DSS requirement section. 

**_<mark>Note:</mark>_** _<mark>Only entities that have legitimate and documented technological or business constraints can consider the use of compensating controls to achieve compliance.</mark>_ 

**Requirement Number and Definition:** 

||**Information Required**|**Explanation**|
|---|---|---|
|**1. Constraints**|Document the legitimate technical or business<br>constraints precluding compliance with the<br>original requirement.||
|**2. Definition of Compensating Controls**|Define the compensating controls: explain how<br>they address the objectives of the original<br>control and the increased risk, if any.||
|**3. Objective**|Define the objective of the original control (for<br>example, the Customized Approach Objective).||
||Identify the objective met by the compensating<br>control_(note: this can be, but is not required to_<br>_be, the stated Customized Approach Objective_<br>_for the PCI DSS requirement)._||
|**4. Identified Risk**|Identify any additional risk posed by the lack of<br>the original control.||
|**5. Validation of Compensating Controls**|Define how the compensating controls were<br>validated and tested.||
|**6. Maintenance**|Define process(es) and controls in place to<br>maintain compensating controls.||



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 371_ 

## **Appendix D Customized Approach** 

This approach is intended for entities that decide to meet a PCI DSS requirement’s stated Customized Approach Objective in a way that does not strictly follow the defined requirement. The customized approach allows an entity to take a strategic approach to meeting a requirement’s Customized Approach Objective, so it can determine and design the security controls needed to meet the objective in a manner unique for that organization. 

**The entity** implementing a customized approach must satisfy the following criteria: 

- Document and maintain evidence about each customized control, including all information specified in the Controls Matrix Template in _PCI DSS v4.x: Sample Templates to Support Customized Approach_ on the PCI SSC website 

- Perform and document a targeted risk analysis (PCI DSS Requirement 12.3.2) for each customized control, including all information specified in the Targeted Risk Analysis Template in _PCI DSS v4.x: Sample Templates to Support Customized Approach_ on the PCI SSC website. 

- Perform testing of each customized control to prove effectiveness, and document testing performed, methods used, what was tested, when testing was performed, and results of testing in the controls matrix. 

- Monitor and maintain evidence about the effectiveness of each customized control. 

- Provide completed controls matrix(es), targeted risk analysis, testing evidence, and evidence of customized control effectiveness to its assessor. 

**The assessor** performing an assessment of customized controls must satisfy the following criteria: 

- Review the entity’s controls matrix(es), targeted risk analysis, and evidence of control effectiveness to fully understand the customized control(s) and to verify the entity meets all Customized Approach documentation and evidence requirements. 

- Derive and document the appropriate testing procedures needed to conduct thorough testing of each customized control. 

- Test each customized control to determine whether the entity’s implementation 1) meets the requirement’s Customized Approach Objective and 2) results in an “in place” finding for the requirement. 

- At all times, QSAs maintain independence requirements defined in the QSA Qualification Requirements. This means if a QSA is involved in designing or implementing a customized control, that QSA does not also derive testing procedures for, assess, or assist with the assessment of that customized control. 

The entity and its assessor are expected to work together to ensure 1) they agree that the customized control(s) fully meets the customized approach objective, 2) the assessor fully understands the customized control, and 3) the entity understands the derived testing the assessor will perform. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 372_ 

Use of the customized approach must be documented by a QSA or ISA in accordance with instructions in the Report on Compliance (ROC) Template and following the instructions in the _FAQs for use with PCI DSS v4.x ROC Template_ available on the PCI SSC website. 

Entities that complete a Self-Assessment Questionnaire are not eligible to use a customized approach; however, these entities may elect to have a QSA or ISA perform their assessment and document it in a ROC Template. 

The use of the customized approach may be regulated by organizations that manage compliance programs (for example, payment brands and acquirers). Therefore, questions about use of a customized approach must be referred to those organizations, including, for example, whether an entity is required to use a QSA, or may use an ISA to complete an assessment using the customized approach. 

**_<mark>Note:</mark>_** _<mark>Compensating controls are not an option with the customized approach. Because the customized approach allows an entity to determine and design the controls needed to meet a requirement’s Customized Approach Objective, the entity is expected to effectively implement the controls it designed for that requirement without needing to also implement alternate, compensating controls.</mark>_ 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 373_ 

## **Appendix E Sample Templates to Support Customized Approach** 

Sample templates to support the Customized Approach (the _Sample Controls Matrix Template_ and _Sample Targeted Risk Analysis Template_ ) provide examples of formats that could be used by entities when documenting their Customized Approach. _While it is not required that entities follow the specific formats provided in these sample templates, the entity’s control matrix and targeted risk analysis must include all the information as defined in these templates._ 

These sample templates are available on the PCI SSC website. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 -2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024_ 

_Page 374_ 

## **Appendix F  Leveraging the PCI Software Security Framework to Support Requirement 6** 

PCI DSS Requirement 6 defines requirements for the development and maintenance of secure systems and software. Because the PCI SSC Secure Software Standard and the Secure SLC Standard (collectively, the Software Security Framework) include rigorous software security requirements, the use of bespoke and custom software that is developed and maintained in accordance with either standard can help the entity to meet several requirements in PCI DSS Requirement 6 without having to perform additional detailed testing, and may also support use of the Customized Approach for other requirements. For details, see Table 7. 

**_<mark>Note</mark>_** _<mark>: This support for meeting Requirement 6 applies only to software that is specifically developed and maintained in accordance with the Secure Software Standard or the Secure SLC Standard; it does not extend to other software or system components in scope for Requirement 6.</mark>_ 

##### **Table 7. Leveraging the PCI Software Security Framework to Support Requirement 6** 

|**PCI DSS Requirements**|**How PCI DSS Requirements Apply to**<br>**Software Developed and Maintained in**<br>**Accordance with the Secure Software**<br>**Standard**|**How PCI DSS Requirements Apply to Software**<br>**Developed and Maintained in Accordance with**<br>**the Secure SLC Standard**|
|---|---|---|
|**6.1**Processes and mechanisms for performing<br>activities in Requirement 6 are defined and<br>understood.|PCI DSS requiremen|ts/objectives apply as usual.|
|**6.2**Bespoke and custom software is developed<br>securely.|PCI DSS Requirement 6.2.4 can be considered in<br>place for software that is developed and<br>maintained in accordance with the Secure<br>Software Standard.|PCI DSS Requirement 6.2 can be considered in place for<br>software that is developed and maintained in accordance<br>with the Secure SLC Standard.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 375_ 

|**PCI DSS Requirements**|**How PCI DSS Requirements Apply to**<br>**Software Developed and Maintained in**<br>**Accordance with the Secure Software**<br>**Standard**|**How PCI DSS Requirements Apply to Software**<br>**Developed and Maintained in Accordance with**<br>**the Secure SLC Standard**|
|---|---|---|
|**6.3**Security vulnerabilities are identified and<br>addressed.|PCI DSS requiremen<br>Software developed and maintained in accordance<br>approach for Req<br>While use of software developed and maintained<br>assurance that the vendor makes security patche<br>**entity retains responsibility**for ensuring that patc<br>req|ts/objectives apply as usual.<br>with the Secure SLC Standard may support the customized<br>uirement 6.3 objectives.<br>in accordance with the Secure SLC Standard provides<br>s and software updates available in a timely manner,**the**<br>hes and updates are installed in accordance with PCI DSS<br>uirements.|
|**6.4**Public-facing web applications are protected<br>against attacks.|PCI DSS requiremen|ts/objectives apply as usual.|
|**6.5**Changes to all system components are<br>managed securely.|PCI DSS requiremen<br>Software developed and maintained in accordance<br>approach for Req<br>While use of software developed and maintained<br>assurance that the vendor follows change managem<br>updates,**the entity retains responsibility**for ensur<br>are implemented into its production enviro|ts/objectives apply as usual.<br>with the Secure SLC Standard may support the customized<br>uirement 6.5 objectives.<br>in accordance with the Secure SLC Standard provides<br>ent procedures during development of software and related<br>ing that software and other changes to system components<br>nment in accordance with PCI DSS requirements.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 376_ 

#### **_Use of Bespoke and Custom Software Developed and Maintained by a Secure SLC Qualified Vendor_** 

When validating the use of software developed and maintained by a Secure SLC Qualified Vendor to meet PCI DSS Requirement 6.2 and support the Customized Approach for Requirements 6.3 and 6.5, the assessor must confirm that the following is met: 

- The software vendor has a current listing on the PCI SSC List of Secure SLC Qualified Vendors—that is, the validation has not expired. 

- The software was developed and is being maintained using software lifecycle management practices that were assessed as part of the software vendor’s validation. 

- The entity is following the implementation guidance provided by the Secure SLC Qualified Vendor. 

#### **_Use of Bespoke and Custom Software Developed in Accordance with the Secure SLC Standard_** 

Entities that internally develop software solely for their use or that develop software for use by a single entity may choose to engage a Secure SLC Assessor to assess their software lifecycle management practices against the Secure SLC Standard. The Secure SLC Assessor will document the results of the assessment in a Secure SLC Report on Compliance (ROC) and a Secure SLC Attestation of Compliance (AOC). 

Software that is developed and maintained following software lifecycle management practices provides the same support for PCI DSS Requirement 6 as software developed and maintained by a Secure SLC Qualified Vendor, if those practices were assessed by a Secure SLC Assessor and confirmed to meet the Secure SLC Standard requirements, with the results documented in a Secure SLC ROC and AOC. 

#### **_Validating the Use of the Secure SLC Standard_** 

When validating the use of software developed and maintained in accordance with the Secure SLC Standard to meet PCI DSS Requirement 6.2 and support customized approach for Requirements 6.3 and 6.5, the assessor must confirm that the following are met: 

- The software lifecycle management practices were assessed by a Secure SLC Assessor and confirmed to meet all Secure SLC Standard requirements with the results documented in a Secure SLC Report on Compliance (ROC) and Secure SLC Attestation of Compliance (AOC). 

- The software was developed and maintained using the software lifecycle management practices covered by the Secure SLC assessment. 

- A full Secure SLC assessment of the software lifecycle management practices was completed within the previous 36 months. Additionally, if the most recent full Secure SLC assessment occurred more than 12 months ago, an Annual Attestation was provided by the developer/vendor within the previous 12 months that confirms continued adherence to Secure SLC Standard for the software lifecycle management practices in use. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 377_ 

#### **_Validating the Use of the Secure Software Standard_** 

When validating the use of software developed and maintained in accordance with the Secure Software Standard to meet PCI DSS Requirement 6.2.4 and support customized approach for Requirements 6.3 and 6.5, the assessor must confirm that the following are met: 

- The secure software assessment was conducted by a Secure Software Assessor and confirmed to meet all requirements in the Secure Software Standard with the results documented in a Secure Software Report on Validation (ROV) and Secure Software Attestation of Validation (AOV). 

- The software was developed and is being maintained using the software lifecycle management practices that were covered by the Secure Software assessment. 

- A full Secure Software assessment was completed within the previous 36 months. Additionally, if the most recent full Secure Software assessment occurred more than 12 months ago, an Annual Attestation was provided by the developer/vendor within the previous 12 months that confirms continued adherence to Secure Software Standard. 

_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 378_ 

## **Appendix G PCI DSS Glossary of Terms, Abbreviations, and Acronyms** 

|**Term**|**Definition**|
|---|---|
|**Account**|Also referred to as “user ID,” “account ID,” or “application ID.” Used to identify an individual or process on a computer system. See<br>_Authentication Credentials_and_Authentication Factor_.|
|**Account Data**|Account data consists of cardholder data and/or sensitive authentication data. See_Cardholder Data_and_Sensitive Authentication_<br>_Data_.|
|**Acquirer**|Also referred to as “merchant bank,” “acquiring bank,” or “acquiring financial institution.” Entity, typically a financial institution, that<br>processes payment card transactions for merchants and is defined by a payment brand as an acquirer. Acquirers are subject to<br>payment brand rules and procedures regarding merchant compliance. See_Payment Processor_.|
|**Administrative**<br>**Access**|Elevated or increased privileges granted to an account for that account to manage systems, networks, and/or applications.<br>Administrative access can be assigned to an individual’s account or a built-in system account. Accounts with administrative access<br>are often referred to as “superuser,” “root,” “administrator,” “admin,” “sysadmin,” or “supervisor-state,” depending on the particular<br>operating system and organizational structure.|
|**AES**|Acronym for “Advanced Encryption Standard.” See_Strong Cryptography._|
|**ANSI**|Acronym for “American National Standards Institute.”|
|**Anti-Malware**|Software that is designed to detect, and remove, block, or contain various forms of malicious software.|
|**AOC**|Acronym for “Attestation of Compliance.” The AOC is the official PCI SSC form for merchants and service providers to attest to the<br>results of a PCI DSS assessment, as documented in a Self-Assessment Questionnaire (SAQ) or Report on Compliance (ROC).|
|**Application**|Includes all purchased, custom, and bespoke software programs or groups of programs, including both internal and external (for<br>example, web) applications.|
|**Application and**<br>**System Accounts**|Also referred to as “service accounts.” Accounts that execute processes or perform tasks on a computer system or in an application.<br>These accounts usually have elevated privileges that are required to perform specialized tasks or functions and are not typically<br>accounts used by an individual.|
|**ASV**|Acronym for “Approved Scanning Vendor.” Company approved by the PCI SSC to conduct external vulnerability scanning services.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 379_ 

|**Term**|**Definition**|
|---|---|
|**Audit Log**|Also referred to as “audit trail.” Chronological record of system activities. Provides an independently verifiable trail sufficient to permit<br>reconstruction, review, and examination of sequence of environments and activities surrounding or leading to operation, procedure, or<br>event in a transaction from inception to final results.|
|**Authentication**|Process of verifying identity of an individual, device, or process. Authentication typically occurs with one or more authentication<br>factors. See_Account, Authentication Credential,_and_Authentication Factor._|
|**Authentication**<br>**Credential**|Combination of the user ID or account ID plus the authentication factor(s) used to authenticate an individual, device, or process. See<br>_Account_and_Authentication Factor._|
|**Authentication Factor**|The element used to prove or verify the identity of an individual or process on a computer system. Authentication typically occurs with<br>one or more of the following authentication factors:<br>•<br>Something you know, such as a password or passphrase,<br>•<br>Something you have, such as a token device or smart card,<br>•<br>Something you are, such as a biometric element.<br>The ID (or account) and authentication factor together are considered authentication credentials. See_Account_and_Authentication_<br>_Credential._|
|**Authorization**|In the context of access control, authorization is the granting of access or other rights to a user, program, or process. Authorization<br>defines what an individual or program can do after successful authentication.<br>In the context of a payment card transaction, authorization refers to the authorization process, which completes when a merchant<br>receives a transaction response (for example, an approval or decline).|
|**BAU**|Acronym for “Business as Usual.”|
|**Bespoke and Custom**<br>**Software**|_Bespoke software_is developed for the entity by a third party on the entity’s behalf and per the entity’s specifications.<br>_Custom software_is developed by the entity for its own use.|
|**Card Skimmer**|A physical device, often attached to a legitimate card-reading device, designed to illegitimately capture and/or store the information<br>from a payment card.|
|**Card Verification**<br>**Code**|Also referred to as Card Validation Code or Value, or Card Security Code. For PCI DSS purposes, it is the three- or four-digit value<br>printed on the front or back of a payment card. May be referred to as CAV2, CVC2, CVN2, CVV2, or CID according to the individual<br>Participating Payment Brands. For more information, contact the Participating Payment Brands.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 380_ 

|**Term**|**Definition**|
|---|---|
|**Cardholder**|Customer to which a payment card is issued, or any individual authorized to use the payment card. See_Visitor._|
|**Cardholder Data**<br>**(CHD)**|At a minimum, cardholder data consists of the full PAN. Cardholder data may also appear in the form of the full PAN plus any of the<br>following: cardholder name, expiration date and/or service code.<br>See_Sensitive Authentication Data_for additional data elements that might be transmitted or processed (but not stored) as part of a<br>payment transaction.|
|**CDE**|Acronym for “Cardholder Data Environment.” The CDE is comprised of:<br>•<br>The system components, people, and processes that store, process, or transmit cardholder data and/or sensitive authentication<br>data, and,<br>•<br>System components that may not store, process, or transmit CHD/SAD but have unrestricted connectivity to system components<br>that store, process, or transmit CHD/SAD.|
|**CERT**|Acronym for “Computer Emergency Response Team.”|
|**Change Control**|Processes and procedures to review, test, and approve changes to systems and software for impact before implementation.|
|**CIS**|Acronym for “Center for Internet Security.”|
|**Cleartext Data**|Unencrypted data.|
|**Column-Level**<br>**Database Encryption**|Technique or technology (either software or hardware) for encrypting contents of a specific column in a database versus the full<br>contents of the entire database. Alternatively, see_Disk Encryption_and_File-Level Encryption_.|
|**Commercial Off-the-**<br>**Shelf (COTS)**|Description of products that are stock items not specifically customized or designed for a specific customer or user and are readily<br>available for use.|
|**Compensating**<br>**Controls**|See PCI DSS Appendices B and C.|
|**Compromise**|Also referred to as “data compromise” or “data breach.” Intrusion into a computer system where unauthorized disclosure/theft,<br>modification, or destruction of cardholder data is suspected.|
|**Console**|Directly connected screen and/or keyboard which permits access and control of a server, mainframe computer, or other system type.<br>See_Non-Console Access_.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 381_ 

|**Term**|**Definition**|
|---|---|
|**Consumer**|Individual cardholder purchasing goods, services, or both.|
|**Critical systems**|A system or technology that is deemed by the entity to be of particular importance. For example, a critical system may be essential for<br>the performance of a business operation or for a security function to be maintained. Examples of critical systems often include<br>security systems, public-facing devices and systems, databases, and systems that store, process, or transmit cardholder data.|
|**Cryptographic**<br>**Algorithm**|Also referred to as “encryption algorithm.” A clearly specified reversible mathematical process used for transforming cleartext data to<br>encrypted data, and vice versa. See_Strong Cryptography._|
|**Cryptographic Key**|A parameter used in conjunction with a cryptographic algorithm that is used for operations such as:<br>•<br>Transforming cleartext data into ciphertext data,<br>•<br>Transforming ciphertext data into cleartext data,<br>•<br>A digital signature computed from data,<br>•<br>Verifying a digital signature computed from data,<br>•<br>An authentication code computed from data, or<br>•<br>An exchange agreement of a shared secret.<br>See_Strong Cryptography._|
|**Cryptographic Key**<br>**Generation**|Key generation is one of the functions within key management. The following documents provide recognized guidance on proper key<br>generation:<br>•<br>_NIST Special Publication 800-133: Recommendation for Cryptographic Key Generation_<br>•<br>_ISO 11568-2 Financial services — Key management (retail) — Part 2: Symmetric ciphers, their key management and life cycle_<br>– 4.3 Key generation<br>•<br>_ISO 11568-4 Financial services — Key management (retail) — Part 4: Asymmetric cryptosystems — Key management and life_<br>_cycle_<br>– 6.2 Key life cycle stages — Generation<br>•<br>_European Payments Council EPC 342-08 Guidelines on Algorithms Usage and Key Management_<br>– 4.1.1 Key generation [for symmetric algorithms]<br>– 4.2.1 Key generation [for asymmetric algorithms].|
|**Cryptographic Key**<br>**Management**|The set of processes and mechanisms which support cryptographic key establishment and maintenance, including replacing older<br>keys with new keys as necessary.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 382_ 

|**Term**|**Definition**|
|---|---|
|**Cryptoperiod**|The time span during which a cryptographic key can be used for its defined purpose. Often defined in terms of the period for which<br>the key is active and/or the amount of ciphertext that has been produced by the key, and according to industry best practices and<br>guidelines (for example,_NIST Special Publication 800-57_).|
|**Customized Approach**|See PCI DSS section:_8 Approaches for Implementing and Validating PCI DSS._|
|**CVSS**|Acronym for “Common Vulnerability Scoring System.” Refer to_ASV Program Guide_for more information.|
|**Data-Flow Diagram**|A diagram showing how and where data flows through an entity’s applications, systems, networks, and to/from external parties.|
|**Default Account**|Login account predefined in a system, application, or device to permit initial access when system is first put into service. Additional<br>default accounts may also be generated by the system as part of the installation process.|
|**Default Password**|Password on system administration, user, or service accounts predefined in a system, application, or device; usually associated with<br>default account. Default accounts and passwords are published and well known, and therefore easily guessed.|
|**Defined Approach**|See PCI DSS section:_8 Approaches for Implementing and Validating PCI DSS._|
|**Disk Encryption**|Technique or technology (either software or hardware) for encrypting all stored data on a device (for example, a hard disk or flash<br>drive). Alternatively, File-Level Encryption or Column-Level Database Encryption is used to encrypt contents of specific files or<br>columns.|
|**DMZ**|Abbreviation for “demilitarized zone.” Physical or logical sub-network that provides an additional layer of security to an organization’s<br>internal private network.|
|**DNS**|Acronym for “Domain Name System.”|
|**Dual Control**|Process of using two or more separate entities (usually persons) operating in concert to protect sensitive functions or information.<br>Both entities are equally responsible for the physical protection of materials involved in vulnerable transactions. No single person is<br>permitted to access or use the materials (for example, the cryptographic key). For manual key generation, conveyance, loading,<br>storage, and retrieval, dual control requires dividing knowledge of the key among the entities. See_Split Knowledge_.|
|**ECC**|Acronym for “Elliptic Curve Cryptography.” See_Strong Cryptography_.|
|**E-commerce (web)**<br>**Redirection Server**|A server that redirects a customer browser from a merchant’s website to a different location for payment processing during an<br>ecommerce transaction.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 383_ 

|**Term**|**Definition**|
|---|---|
|**Encryption**|The (reversible) transformation of data by a cryptographic algorithm to produce cipher text, i.e., to hide the information content of the<br>data. See_Strong Cryptography_.|
|**Encryption Algorithm**|See_Cryptographic Algorithm_.|
|**Entity**|In the context of a PCI DSS assessment, a term used to represent the corporation, organization, or business which is undergoing an<br>assessment.|
|**File Integrity**<br>**Monitoring (FIM)**|A change-detection solution that checks for changes, additions, and deletions to critical files, and notifies when such changes are<br>detected.|
|**File-Level Encryption**|Technique or technology (either software or hardware) for encrypting the full contents of specific files. Alternatively, see_Disk_<br>_Encryption_and_Column-Level Database Encryption_.|
|**Firewall**|Hardware and/or software technology that protects network resources from unauthorized access. A firewall permits or denies<br>computer traffic between networks with different security levels based upon a set of rules and other criteria.|
|**Forensics**|Also referred to as “computer forensics.” As it relates to information security, the application of investigative tools and analysis<br>techniques to gather evidence from computer resources to determine the cause of data compromises.<br>Investigations into compromises of payment data are typically conducted by a PCI Forensic Investigator (PFI).|
|**FTP**|Acronym for “File Transfer Protocol.” Network protocol used to transfer data from one computer to another through a public network<br>such as the Internet. FTP is widely viewed as an insecure protocol because passwords and file contents are sent unprotected and in<br>cleartext. FTP can be implemented securely via SSH or other technology.|
|**Hashing**|A method to protect data that converts data into a fixed-length message digest. Hashing is a one-way (mathematical) function in<br>which a non-secret algorithm takes any arbitrary length message as input and produces a fixed length output (usually called a “hash<br>code” or “message digest”). Hash functions are required to have the following properties:<br>•<br>It is computationally infeasible to determine the original input given only the hash code,<br>•<br>It is computationally infeasible to find two inputs that give the same hash code.|
|**HSM**|Acronym for “hardware security module” or “host security module.” A physically and logically protected hardware device that provides<br>a secure set of cryptographic services, used for cryptographic key-management functions and/or the decryption of account data.|
|**IDS**|Acronym for “intrusion-detection system.”|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 384_ 

|**Term**|**Definition**|
|---|---|
|**Index Token**|A random value from a table of random values that corresponds to a given PAN.|
|**Interactive Login**|The process of an individual providing authentication credentials to directly log into an application or system account. Using<br>interactive login means there is no accountability or traceability of actions taken by that individual.|
|**IPS**|Acronym for “intrusion prevention system.”|
|**ISO**|Acronym for “International Organization for Standardization.”|
|**Issuer**|Also referred to as “issuing bank” or “issuing financial institution.” Entity that issues payment cards or performs, facilitates, or supports<br>issuing services, including but not limited to issuing banks and issuing processors.|
|**Issuing services**|Examples of issuing services include but are not limited to authorization and card personalization.|
|**Keyed Cryptographic**<br>**Hash**|A hashing function that incorporates a randomly generated secret key to provide brute force attack resistance and secret<br>authentication integrity.<br>Appropriate keyed cryptographic hashing algorithms include but are not limited to: HMAC, CMAC, and GMAC, with an effective<br>cryptographic strength of at least 128-bits (_NIST SP 800-131Ar2)_.<br>Refer to the following for more information about HMAC, CMAC, and GMAC, respectively:_NIST SP 800-107r1, NIST SP 800-38B,_<br>_and NIST SP 800-38D)._<br>See_NIST SP 800-107 (Revision 1): Recommendation for Applications Using Approved Hash Algorithms_§5.3.|
|**Key Custodian**|A role where a person(s) is entrusted with, and responsible for, performing key management duties involving secret and/or private<br>keys, key shares, or key components on behalf of an entity.|
|**Key Management**<br>**System**|A combination of hardware and software that provides an integrated approach for generating, distributing, and/or managing<br>cryptographic keys for devices and applications.|
|**LAN**|Acronym for “local area network.”|
|**LDAP**|Acronym for “Lightweight Directory Access Protocol.”|
|**Least Privileges**|The minimum level of privileges necessary to perform the roles and responsibilities of the job function.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 385_ 

|**Term**|**Definition**|
|---|---|
|**Legal Exception**|A legal restriction due to a local or regional law, regulation, or regulatory requirement, where meeting a PCI DSS requirement would<br>violate that law, regulation, or regulatory requirement. Contractual obligations or legal advice are**not**legal restrictions.<br>See the following PCI DSS v4.x documents for information on reporting legal exceptions:<br>•<br>_The Report on Compliance (ROC) Template_and related_Attestations of Compliance_.<br>•<br>_The Self-Assessment Questionnaires (SAQs)_and related_Attestations of Compliance_.<br>_Note: Where an entity operates in multiple locations, a legal exception may only be claimed for the locations governed by the law,_<br>_regulation, or regulatory requirement, and may not be claimed for locations in which such law, regulation, or regulatory requirement is_<br>_inapplicable._|
|**Log**|See_Audit Log_.|
|**Logical Access**<br>**Control**|Mechanisms that limit the availability of information or information-processing resources only to authorized persons or applications.<br>See_Physical Access Control_.|
|**MAC**|In cryptography, an acronym for “message authentication code.” See_Strong Cryptography_.|
|**Magnetic-Stripe Data**|See_Track Data_.|
|**Masking**|Method of concealing a segment of PAN when displayed or printed. Masking is used when there is no business need to view the<br>entire PAN. Masking relates to protection of PAN when displayed on screens, paper receipts, printouts, etc.<br>See_Truncation_for protection of PAN when electronically stored, processed, or transmitted.|
|**Media**|Physical material, including but not limited to, electronic storage devices, removable electronic media, and paper reports.|
|**Merchant**|For the purposes of the PCI DSS, a merchant is defined as any entity that accepts payment cards bearing the logos of any PCI SSC<br>Participating Payment Brand as payment for goods and/or services.<br>A merchant that accepts payment cards as payment for goods and/or services can also be a service provider, if the services sold<br>result in storing, processing, or transmitting cardholder data on behalf of other merchants or service providers. For example, an ISP is<br>a merchant that accepts payment cards for monthly billing, but also is a service provider if it hosts merchants as customers.|
|**MO/TO**|Acronym for “Mail-Order/Telephone-Order.”|
|**Multi-Factor**<br>**Authentication**|Method of authenticating a user whereby at least two factors are verified. These factors include something the user has (such as a<br>smart card or dongle), something the user knows (such as a password, passphrase, or PIN), or something the user is or does (such<br>as fingerprints and other biometric elements).|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 386_ 

|**Term**|**Definition**|
|---|---|
|**Multi-Tenant Service**<br>**Provider**|A type of Third-Party Service Provider that offers various shared services to merchants and other service providers, where customers<br>share system resources (such as physical or virtual servers), infrastructure, applications (including Software as a Service (SaaS)),<br>and/or databases. Services may include, but are not limited to, hosting multiple entities on a single shared server, providing e-<br>commerce and/or “shopping cart” services, web-based hosting services, payment applications, various cloud applications and<br>services, and connections to payment gateways and processors. See_Service Provider_and_Third-Party Service Provider_.|
|**NAC**|Acronym for “Network Access Control.”|
|**NAT**|Acronym for “Network Address Translation.”|
|**Network Connection**|A logical, physical, or virtual communication path between devices that allows the transmission and reception of network layer<br>packets.|
|**Network Diagram**|A diagram showing system components and connections within a networked environment.|
|**Network Security**<br>**Controls (NSC)**|Firewalls and other network security technologies that act as network policy enforcement points. NSCs typically control network traffic<br>between two or more logical or physical network segments (or subnets) based on pre-defined policies or rules.|
|**NIST**|Acronym for “National Institute of Standards and Technology.” Non-regulatory federal agency within U.S. Commerce Department's<br>Technology Administration.|
|**Non-Console Access**|Logical access to a system component that occurs over a network interface rather than via a direct, physical connection to the system<br>component. Non-console access includes access from within local/internal networks as well as access from external or remote<br>networks.|
|**NTP**|Acronym for “Network Time Protocol.”|
|**Organizational**<br>**Independence**|An organizational structure that ensures there is no conflict of interest between the person or department performing the activity and<br>the person or department assessing the activity. For example, individuals performing assessments are organizationally separate from<br>the management of the environment being assessed.|
|**OWASP**|Acronym for “Open Web Application Security Project.”|
|**PAN**|Acronym for “primary account number.” Unique payment card number (credit, debit, or prepaid cards, etc.) that identifies the issuer<br>and the cardholder account.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 387_ 

|**Term**|**Definition**|
|---|---|
|**Password /**<br>**Passphrase**|A string of characters that serve as an authentication factor for a user or account.|
|**Patch**|Update to existing software to add function or to correct a defect.|
|**Participating Payment**<br>**Brand**|Also referred to as “payment brand.” A payment card brand that, as of the time in question, is then formally admitted as (or an affiliate<br>of) a member of PCI SSC pursuant to its governing documents. At the time of writing, Participating Payment Brands include PCI SSC<br>Founding Members and Strategic Members.|
|**Payment Brand**|An organization with branded payment cards or other payment card form factors. Payment brands regulate where and how the<br>payment cards or other form factors carrying its brand or logo are used. A payment brand may be a PCI SSC Participating Payment<br>Brand or other global or regional payment brand, scheme, or network.|
|**Payment Card Form**<br>**Factor**|Includes physical payment cards as well as devices with functionality that emulates a payment card to initiate a payment transaction.<br>Examples of such devices include, but are not limited to, smartphones, smartwatches, fitness bands, key tags, and wearables such as<br>jewelry.|
|**Payment Cards**|For purposes of PCI DSS, any payment card form factor that bears the logo of any PCI SSC Participating Payment Brand.|
|**Payment Channel**|Methods used by merchants to accept payments from customers. Common payment channels include card present (in person) and<br>card not present (e-commerce and MO/TO).|
|**Payment Page**|A web-based user interface containing one or more form elements intended to capture account data from a consumer or submit<br>captured account data, for purposes of processing and authorizing payment transactions. The payment page can be rendered as any<br>one of:<br>•<br>A single document or instance,<br>•<br>A document or component displayed in an inline frame within a non-payment page,<br>•<br>Multiple documents or components each containing one or more form elements contained in multiple inline frames within a non-<br>payment page.|
|**Payment Page Scripts**|Any programming language commands or instructions on a payment page that are processed and/or interpreted by a consumer’s<br>browser, including commands or instructions that interact with a page’s document object model. Examples of programming languages<br>are JavaScript and VB script; neither markup-languages (for example, HTML) or style-rules (for example, CSS) are programming<br>languages.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 388_ 

|**Term**|**Definition**|
|---|---|
|**Payment Processor**|Sometimes referred to as “payment gateway” or “payment service provider (PSP).” Entity engaged by a merchant or other entity to<br>handle payment card transactions on their behalf. See_Acquirers._|
|**PCI DSS**|Acronym for “Payment Card Industry Data Security Standard.”|
|**Personnel**|Full-time and part-time employees, temporary employees, contractors, and consultants with security responsibilities for protecting<br>account data or that can impact the security of cardholder data and/or sensitive authentication data. See_Visitor._|
|**Phishing Resistant**<br>**Authentication**|Authentication designed to prevent the disclosure and use of authentication secrets to any party that is not the legitimate system to<br>which the user is attempting to authenticate (for example, through in-the-middle (ITM) or impersonation attacks). Phishing-resistant<br>systems often implement asymmetric cryptography as a core security control.<br>Systems that rely solely on knowledge-based or time-limited factors such as passwords or one-time-passwords (OTPs) are not<br>considered phishing resistant, nor are SMS or magic links. Examples of phishing-resistant authentication includes FIDO2.|
|**Physical Access**<br>**Control**|Mechanisms that limit the access to a physical space or environment to only authorized persons. See_Logical Access Control_.|
|**PIN**|Acronym for “personal identification number.”|
|**PIN Block**|A block of data used to encapsulate a PIN during processing. The PIN block format defines the content of the PIN block and how it is<br>processed to retrieve the PIN. The PIN block is composed of the PIN, the PIN length, and may contain the PAN (or a truncation<br>thereof) depending on the approved ISO PIN Block Format used.|
|**POI**|Acronym for “Point of Interaction,” the initial point where data is read from a card.|
|**Point of Sale System**<br>**(POS)**|Hardware and software used by merchants to accept payments from customers. May include POI devices, PIN pads, electronic cash<br>registers, etc.|
|**Privileged User**|Any user account with greater than basic access privileges. Typically, these accounts have elevated or increased privileges with more<br>rights than a standard user account. However, the extent of privileges across different privileged accounts can vary greatly depending<br>on the organization, job function or role, and the technology in use.|
|**QIR**|Acronym for “Qualified Integrator or Reseller.” Refer to the_QIR Program Guide_on the PCI SSC website for more information.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 389_ 

|**Term**|**Definition**|
|---|---|
|**QSA**|Acronym for “Qualified Security Assessor.” QSA companies are qualified by PCI SSC to validate an entity’s adherence to PCI DSS<br>requirements. Refer to the_QSA Qualification Requirements_for details about requirements for QSA Companies and Employees.|
|**Remote Access**|Access to an entity’s network from a location outside of that network. An example of technology for remote access is a VPN.|
|**Removable Electronic**<br>**Media**|Media that stores digitized data that can be easily removed and/or transported from one computer system to another. Examples of<br>removable electronic media include CD-ROM, DVD-ROM, USB flash drives, and external/portable hard drives. In this context,<br>removable electronic media does not include hot-swappable drives, tape drives used for bulk back-ups, or other media not typically<br>used to transport data from one location for use in another.|
|**Risk Assessment**|Enterprise-wide process that identifies valuable system resources and threats; quantifies loss exposures (that is, loss potential) based<br>on estimated frequencies and costs of occurrence; and (optionally) recommends how to allocate resources to countermeasures to<br>minimize total exposure. See_Targeted Risk Analysis_.|
|**Risk Ranking**|Process of classifying risks to identify, prioritize, and address items in the order of importance.|
|**ROC**|Acronym for “Report on Compliance.” Reporting tool used to document detailed results from an entity’s PCI DSS assessment.|
|**RSA**|Algorithm for public-key encryption. See_Strong Cryptography_.|
|**SAQ**|Acronym for “Self-Assessment Questionnaire.” Reporting tool used to document self-assessment results from an entity’s PCI DSS<br>assessment.|
|**Scoping**|Process of identifying all system components, people, and processes to be included in a PCI DSS assessment. See PCI DSS section:<br>_4 Scope of PCI DSS Requirements_.|
|**Secure Coding**|The process of creating and implementing applications that are resistant to tampering and/or compromise.|
|**Security Event**|An occurrence considered by an organization to have potential security implications to a system or its environment. In the context of<br>PCI DSS, security events identify suspicious or anomalous activity.|
|**Security Officer**|Primary person responsible for an entity’s security.|
|**Segmentation**|Also referred to as “network segmentation” or “isolation.” Segmentation isolates system components that store, process, or transmit<br>cardholder data from systems that do not. See “Segmentation” in PCI DSS section:_4 Scope of PCI DSS Requirements_.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 390_ 

|**Term**|**Definition**|
|---|---|
|**Sensitive Area**|A sensitive area is typically a subset of the CDE and is any area that houses systems considered critical to the CDE. This includes<br>data centers, server rooms, back-office rooms at retail locations, and any area that concentrates or aggregates cardholder data<br>storage, processing, or transmission. Sensitive areas also include areas housing systems that manage or maintain the security of the<br>CDE (for example, those providing network security controls or that manage physical or logical security).<br>This excludes the areas where only point-of-sale terminals are present, such as the cashier areas in a retail store or call centers<br>where agents are taking payments.|
|**Sensitive**<br>**Authentication Data**<br>**(SAD)**|Security-related information used to authenticate cardholders and/or authorize payment card transactions. This information includes,<br>but is not limited to, card verification codes, full track data (from magnetic stripe or equivalent on a chip), PINs, and PIN blocks.|
|**Separation of Duties**|Practice of dividing steps in a function among multiple individuals, to prevent a single individual from subverting the process.|
|**Service Code**|Three-digit or four-digit value in the magnetic-stripe that follows the expiration date of the payment card on the track data. It is used<br>for various things, such as defining service attributes, differentiating between international and national interchange, or identifying<br>usage restrictions.|
|**Service Provider**|Business entity that is not a payment brand, directly involved in the processing, storage, or transmission of cardholder data (CHD)<br>and/or sensitive authentication data (SAD) on behalf of another entity. This includes payment gateways, payment service providers<br>(PSPs), and independent sales organizations (ISOs). This also includes companies that provide services that control or could impact<br>the security of  CHD and/or SAD. Examples include managed service providers that provide managed firewalls, IDS, and other<br>services as well as hosting providers and other entities.<br>If an entity provides a service that involves_only_the provision of public network access—such as a telecommunications company<br>providing just the communication link—the entity would not be considered a service provider for that service (although they may be<br>considered a service provider for other services). See_Multi-Tenant Service Provider_and_Third-Party Service Provider._|
|**SNMP**|Acronym for “Simple Network Management Protocol.”.|
|**Split Knowledge**|A method by which two or more entities separately have key components or key shares that individually convey no knowledge of the<br>resultant cryptographic key.|
|**SQL**|Acronym for “Structured Query Language.”|
|**SSH**|Abbreviation for “Secure Shell.”|
|**SSL**|Acronym for “Secure Sockets Layer.”|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

|_June 2024_|
|---|
|_Page 391_|



|**Term**|**Definition**|
|---|---|
|**Strong Cryptography**|Cryptography is a method to protect data through a reversible encryption process, and is a foundational primitive used in many<br>security protocols and services. Strong cryptography is based on industry-tested and accepted algorithms along with key lengths that<br>provide a minimum of 112-bits of effective key strength and proper key-management practices_._<br>Effective key strength can be shorter than the actual ‘bit’ length of the key, which can lead to algorithms with larger keys providing<br>lesser protection than algorithms with smaller actual, but larger effective, key sizes._It is recommended that all new implementations_<br>_use a minimum of 128-bits of effective key strength._<br>Examples of industry references on cryptographic algorithms and key lengths include:<br>•<br>_NIST Special Publication 800-57 Part 1,_<br>•<br>_BSI TR-02102-1,_<br>•<br>_ECRYPT-CSA D5.4 Algorithms, Key Size and Protocols Report (2018), and_<br>•<br>_ISO/IEC 18033 Encryption algorithms, and_<br>•<br>_ISO/IEC 14888-3:2-81 IT Security techniques – Digital signatures with appendix – Part 3: Discrete logarithm based mechanisms_.|
|**System Components**|Any network devices, servers, computing devices, virtual components, or software included in or connected to the CDE, or that could<br>impact the security of cardholder data and/or sensitive authentication data.|
|**System-level object**|Anything on a system component that is required for its operation, including but not limited to application executables and<br>configuration files, system configuration files, static and shared libraries and DLLs, system executables, device drivers and device<br>configuration files, and third-party components.|
|**Targeted Risk**<br>**Analysis**|For PCI DSS purposes, a risk analysis that focuses on a specific PCI DSS requirement(s) of interest, either because the requirement<br>allows flexibility (for example, as to frequency) or, for the Customized Approach, to explain how the entity assessed the risk and<br>determined the customized control meets the objective of a PCI DSS requirement.|
|**TDES**|Acronym for “Triple Data Encryption Standard.” Also referred to as “3DES” or “Triple DES.”|
|**Telnet**|Abbreviation for “telephone network protocol.”|
|**Third-Party Service**<br>**Provider (TPSP)**|Any third party acting as a service provider on behalf of an entity. See_Multi-Tenant Service Provider_and_Service Provider_.|
|**Third-Party Software**|Software that is acquired by, but not developed expressly for, an entity. It may be open source, freeware, shareware, or purchased.|
|**TLS**|Acronym for “Transport Layer Security.”|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 392_ 

|**Term**|**Definition**|
|---|---|
|**Token**|In the context of authentication and access control, a token is a value provided by hardware or software that works with an<br>authentication server or VPN to perform dynamic or multi-factor authentication.|
|**Track Data**|Also referred to as “full track data” or “magnetic-stripe data.” Data encoded in the magnetic stripe or chip used for authentication<br>and/or authorization during payment transactions. Can be the magnetic-stripe image on a chip or the track data on the magnetic<br>stripe.|
|**Truncation**|Method of rendering a full PAN unreadable by removing a segment of PAN data. Truncation relates to protection of PAN when<br>electronically stored, processed, or transmitted.<br>See_Masking_for protection of PAN when displayed on screens, paper receipts, etc.|
|**Trusted Network**|Network of an entity that is within the entity’s ability to control or manage and that meets applicable PCI DSS requirements.|
|**Untrusted Network**|Any network that does not meet the definition of a “trusted network.”|
|**Virtual Payment**<br>**Terminal**|In the context of Self-Assessment Questionnaire (SAQ) C-VT, a virtual payment terminal is web-browser-based access to an acquirer,<br>processor, or third-party service provider website to authorize payment card transactions, where the merchant manually enters<br>payment card data through a web browser. Unlike physical terminals, virtual payment terminals do not read data directly from a<br>payment card. Because payment card transactions are entered manually, virtual payment terminals are typically used instead of<br>physical terminals in merchant environments with low transaction volumes.|
|**Virtualization**|The logical abstraction of computing resources from physical and/or logical constraints. One common abstraction is referred to as<br>virtual machines or VMs, which takes the content of a physical machine and allows it to operate on different physical hardware and/or<br>along with other virtual machines on the same physical hardware. Other common abstractions include, but are not limited to,<br>containers, serverless computing, or microservices.|
|**Visitor**|A vendor, guest of any personnel, service worker, or personnel that normally do not have access to the subject area.<br>Cardholders present in a retail location to purchase goods or services are not considered “visitors.” See_Cardholder_and_Personnel._|
|**VPN**|Acronym for “virtual private network.”|
|**Vulnerability**|Flaw or weakness which, if exploited, may result in an intentional or unintentional compromise of a system.|
|**Web Application**|An application that is generally accessed through a web browser or through web services. Web applications may be available through<br>the Internet or a private, internal network.|



_Payment Card Industry Data Security Standard: Requirements and Testing Procedures, v4.0.1 © 2006 - 2024 PCI Security Standards Council, LLC. All rights reserved._ 

_June 2024 Page 393_ 

