---
title: "Demo"
permalink: /docs/demo/
excerpt: "What is and how to use a Prompt sail demo"
last_modified_at: 2024-07-10T12:46:35+01:00
redirect_from:
  - /theme-setup/
toc: true
toc_sticky: true
---


## Prompt Sail demo


Experience the functionalities of Prompt Sail firsthand by utilizing our [**demo**](https://try-promptsail.azurewebsites.net/). 
{: .notice--warning}

**No installation or account creation is required, making it a straightforward process.**


The demo provides an insight into the user interface of Prompt Sail, and its architecture, and allows to test the capture of the transactions (Gen AI model calls).

To logg your AI API call in the demo:

1. Visit [**demo page**](https://try-promptsail.azurewebsites.net/).
2. Access the list of projects by clicking the "Get Started" button. (No account creation or login is required.)
3. Select an existing project or create a new one.
4. Obtain the proxy URL required to initiate the logging of calls to Gen AI models.
   1. In the Project Dashboard, navigate to the AI Providers tab. Select an available deployment. or create your own if the required provider is not listed.
   2. Copy the auto-generated proxy URL and integrate it into your script/application that communicates with the chosen Gen AI model. 
5. Execute your script/application with the proxy URL and return to the Prompt Sail demo.
6. In the Project Dashboard, under the Transactions tab, you will see a table containing transactions, including the one from your AI API call. 
7. By clicking on the transaction ID, you will go to its details.  
8. Whereas the Overview tab provides a comprehensive view of all transaction statistics for the project.

**Warning**: The Prompt Sail demo is public, so avoid including any sensitive information in your prompts when testing the demo. Each new deployment of [**demo page**](https://try-promptsail.azurewebsites.net/) resets the database, causing projects and transactions in the demo to be regularly deleted.
{: .notice--warning}
