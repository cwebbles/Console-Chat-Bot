
## AI For Education

### Specs
I'm pretty sure Dr. Bean wants us to build a framework/platform 
with the ability to take in curriculum and have AI walk students
through the course. I think he wants a way to upload curriculum,
a platform that can handle that curriculum and parse it into its
several 'modules' and then create a course layout for students to
go through with the help of AI. I have a few rough idea about 
features and how we can make this work

- Canvas integration
- Ability to upload curriculum in a specific format
- Framework-first design that allows for simple configuration and extension
- Classes designed to hold questions, lessons, quizzes, problems, etc.
- Deployed on AWS lambda using API gateway
- We can start by just using discord
- Terraform IAC deployment

### Vision
My first take on what our end goal might be is integrating this system with
Discord and giving the chatbot a command for a certain lesson/question
and then 'running' that portion of the course with AI walking the
student through the material

### Knowns
These are the things that I do know and will be able to do:

- AWS Lambdas, API Gateway
- Some terraform
- Integration with Chat
- Python (kind of)
- Discord chatbots


### Known Unknowns
There are a few things I know I don't know and could cause problems

- How to run code snippets in the cloud
- How to get AI to walk a student through a course
- Exact terraform deployment
- Quest

### Basic User Experience

1. User access platform (discord) and makes a curriculum request
2. Request is sent to API Gateway, then Lambda, and the request is processed
3. The Lambda accesses the database, retrieves relevant curriculum information
4. Lambda preps 'lesson' and connects with Rubber Duck to prepare to teach
5. User *interacts with lesson* and Rubber Duck through question and answer and hint process
6. User completes lesson

### Questions
We may need to flesh out a few of the following things

- How are we going to track a users progress in a lesson?
- How will we notify AI of where the user is currently in the process
- How will Quest fit into this?
- How do we want to design the curriculum to make it easily progress-able and easy to understand for RD?

### Study
Lang Chain