# DSGO service catalogue (Stelselcatalogus)

## Introduction
This repository is the backend of the DSGO prototype service catalogue, a curated list of data services designed to facilitate easy access and discovery for those seeking DSGO based data services.

## Instructions for Data Service Providers (currently only possible for DSGO adoptieprojecten)

If you are a data service provider looking to include your service in our catalogue, please adhere to the following process:

- **Email the Admin**: Initiate your request by sending an email to [afsprakenstelseldsgo@digigo.nu] with the subject line "Inclusion Request for Data Services Catalogue." Provide a comprehensive description of your service in line with the DSGO afsprakenstelsel.
  
- **Await Confirmation**: Post-submission, your application will be evaluated based on relevance and utility. The admin will contact you for any additional information needed or to communicate the outcome of your request.

## Instructions for Admin

As an admin, you have the authority to manage the listings within the repository. Here are detailed instructions on how to do so:

### Adding a Data Service

- **Data Service Entry**: Navigate to the `data_services_list.json` file and insert a new entry for the data service. Assign a unique identifier to each service and provide a succinct yet descriptive overview of the service offerings.
  
  ```json
  {
    "service_id": "unique_service_identifier",
    "feature": "Service Name",
    "description": "Brief description of the service."
    // Add additional service details as needed
  }
  ```
- **Logo upload**: Store service logos within the images directory. Logos should be in .png format to ensure compatibility with the website's automated deployment system, which will process the image to have a white background and reshape it to a square for uniformity.
- **Removing a data service**: To remove a service, delete the corresponding entry from the data_services_list.json. Additionally, you need to remove any associated service files from the _services folder to prevent orphaned references.
