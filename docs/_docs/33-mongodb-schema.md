---
title: "Monodb database schema"
permalink: /docs/database-schema/
excerpt: "How the database schema was designed."
last_modified_at: 2024-04-228T18:48:35+01:00
redirect_from:
  - /theme-setup/
toc: true
---

## Why we chose MongoDB

We chose MongoDB because it is a NoSQL database that is easy to scale and manage. It is also very flexible and can store data in a variety of formats. This makes it ideal for storing the unstructured data that is generated by the Prompt Sail application.


## Database schema

There are three main objects in the database: `projects`, `transactions`, and `settings`. Each of them has a similar structure. 

The `projects` table is the most important because it is the parent of the other two. 

The `transactions` table is the most numerous because each user request creates a new transaction. 






### Projects

todo


### Transactions

todo







