## Grade Summary (Group): 

- Quality of Planning Document: 85
- Quality of Requirements (in Kanban): 83

Combined Grade: 84

## Planning Document Feedback (Group): 

- You have a good start on your system description. However, you need to explain more about the use case in the context of the overall Picobytes application. This system description is meant to get you thinking about your abstract for the Rhodes Symposium. It should explain why the system is needed in addition to what it does at a high level. Also, you definitely want to mention that this is for the execution of C programs and test cases in your description. Right now, it sounds like you could execute any kind of program.
- You have two sections called system description in your document.
- Minimally, your system diagram should show each of your system components. You list API gateway, sandbox manager, compiler/executor, result aggregator, and logging as components, but your system diagram shows clients, server, and containers. You need to connect the dots here. This is also where you should explain the purpose of each of these components.
- Your epics need some work. Remember that epics are just big user stories. They should be structured that way. All of the functionality from your app is only usable if it is accessible via an API, so you shouldn't separate API out as a separate thing. 'Execute C code' would assume input of source code to your API and program/compiler output from your API. 'Test case execution' assumes input of code and test cases to your API and output of test case results from your API. Epic 5 sounds more like a set of non- functional requirements.
- You have some decent non- functional requirements, but a few could use some revisions. For example, the application should scale to handle what? Maybe 50 simultaneous compile requests? Also, what does 'Resource Management' mean?
- Your technologies list seems pretty non- commital. I can understand if you have some uncertainty related to containerization and the managed environment, but why do you list Django, Flask, and FastAPI? They all serve the same purpose and there isn't any real risk related to choosing one of those. Also need to choose a C compiler.
- Your MVP looks very reasonable.
- Your roadmap isn't much of a roadmap. You should be trying to take your applications features and identify the sprint when you plan on implementing those features. In the instructions I stated, 'there are six development sprints with pre- defined dates. Use these to structure your roadmap.' You should also be showing where in the sprints (which sprint number) you plan on completing your MVP.

## Requirements Feedback (Group): 

- I think you have some tasks that are masquerading as user stories. US1, US7, and US11 seem like tasks for the same user story. Same with US3 and US14.
- US4 and US9 seem to have a lot of overlap. Are these distinct stories? 
- US12 seems like a non- functional requirement. 
- Your titles are consistent and generally easy to understand.
- All of your user stories are traceable to an epic, which is great.
- You have acceptance criteria for all of your sprint 1, which is a start, but its not clear how some of this will be tested. For example, how are you planning to test US1 and US2? Are you printing something in the logs or to the console?
- I don't see any estimates on the level of effort for your stories. I think adding these would help you better plan your sprints and the division of labor within your group.
- You seem to have done some prioritization, but its hard to relate it directly to your roadmap.
