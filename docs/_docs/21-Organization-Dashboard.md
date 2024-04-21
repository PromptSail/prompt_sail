---
title: "Organization Dashboard"
permalink: /docs/organization-dashboard/
excerpt: "The Organization Dashboard page serves as a central hub for managing projects within the organization"
last_modified_at: 2024-02-01T14:06:00+01:00
redirect_from:
    - /theme-setup/
toc: true
---

The Organization Dashboard page serves as a central hub for managing projects within the organization. It provides users with easy access to all pertinent project information and enables quick searching and creation of new projects.
This page can be accessed at `localhost:80` after logging in to the application.

<img src='docs/assets/images/Organization_Dashboard.png' />

### Interface Elements:

-   **Project List:**

    -   Displays a list of all projects belonging to the organization.
    -   Each project is represented by a container containing basic information such as name, description, tags, etc.
    -   Clicking on a project opens the Project Dashboard, where users can access detailed information and manage the project.

-   **Search bar:**

    -   Allows users to quickly find a specific project by entering search criteria such as name, slug, description, or tags.
    -   Search is performed live, dynamically filtering the project list as the user types their query.

-   **"New Project" Button:**
    -   Clicking the button opens the new project wizard, which guides the user through the process of creating a new project.
    -   The wizard enables users to specify all necessary information about the new project, such as name, description, tags, etc.

### Notes:

-   The Organization Dashboard page serves as the starting point for users of the application, providing them with quick access to all essential project management functions.
