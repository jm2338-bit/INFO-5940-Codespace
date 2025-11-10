# Assignemnt 2 Reflection
This assignment was a practical application of multi-agent workflows. The main takeaway was the power of separation of concerns. By splitting the job between a creative "Planner" and an analytical "Reviewer," the system became both imaginative and factually grounded. The Planner didn't have to worry about being wrong, and the Reviewer had a clear, focused job to find and fix the errors.

The "propose-and-refine" pattern works very well. The Planner was free to brainstorm a full, plausible itinerary without the internet. Its "hallucinations" on details like museum hours or prices became a feature. It gave the Reviewer a solid structure to fact check. The Reviewer then did the important work of validating the plan. This feels really like a human process. We write a draft, then edit it for accuracy.

The biggest challenge was prompt engineering. At first, I was a little stumbled by how much detail I needed to give the agents for them to do their jobs well. A simple "review this" prompt for the Reviewer was too vague. It might just get a lazy "looks good" or it might make corrections without explaining what it changed and the rationale. The solution was mandating a specific output format. I required the Reviewer to produce a "Delta List." This forced it to first list all concrete changes and the reasons for them.

A future idea would be to add a loop. The Reviewer could send its "Delta List" back to the Planner and generate a corrected version. 

I used GenAI to summarize the reference log and word it better.

