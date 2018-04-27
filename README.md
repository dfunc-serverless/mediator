# mediator
---
API engine
## Dependency
- Flask
- Mongo
- Redis
- bson
## Feature
- Create worker
- Add job
- Register worker
- Register job
## Usage
This applciation is paired with MongoDB. All information needed for communicating with Google Pubsub is handeled by mediator. All jobs are queueed by the mediator in one queue with status: in queue, Excuting, Completed, and Failed. 

To run this component please see [setup](https://github.com/dfunc-serverless/setup).
## Future Work
Jobs are not queued in a way that inspires efficient distribution. All jobs are treated equally without priority. This can be changed by getting more informaiton of the job such as docker image size, function excution time, and required resources.