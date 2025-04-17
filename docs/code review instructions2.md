### Code Review Instructions
## Purpose
This document provides detailed instructions for conducting code reviews in this repository. Following these guidelines ensures code quality, consistency, and adherence to best practices.

## Instructions
Do not apply changes during code review unless specifically told to.

## General Guidelines:

Ensure the code is clean, readable, and follows consistent formatting.
Verify that meaningful variable, method, and class names are used.
Check for modularity and adherence to the single responsibility principle.
Documentation:

Ensure public interface methods have Javadoc comments.
Verify that inline comments are used sparingly and only when necessary.
Error Handling:

Check for proper error handling using custom exceptions.
Ensure meaningful error messages are logged with context.
Testing:

Verify that unit tests cover all service and repository layers.
Ensure integration tests are written for critical workflows.
Spring Boot Specific Rules:

Check for proper use of dependency injection (constructor-based preferred).
Verify that configuration values are externalized in application.yml or application.properties.
Tech debts
Code should not have commented pieces of code or TODO/Fixme marks - usually that means that author did not complete some requirement.

Code should not have unused variables, methods or unreachable code blocks.

Code should not have empty methods, block, classes or some sort of UnsupportedOperationException throws.

## Code structure
Related classes should be grouped in packages by using Hexagonal approach (including inside src/main, src/test, src/integrationTest).

Avoid using interfaces for service classes if they will likely never have multiple implementations. In such scenario interfaces become an unnecessary layer of abstraction and can add complexity to the code with no apparent benefit.

## Maintainability
Does the code covered with tests?

Does the code comply with the accepted Best Practices?

Key interfaces/classes or public methods are good candidates to have Javadoc

The following things should be aligned during code review: - Unobvious code fragments: should be rewritten with better design/structure/common patterns - Complex algorithms: should be re-arranged/simplified where possible - All variables/methods/classes/packages/modules/extensions that are not self-describing: should be renamed to better names - Code that has been optimized or modified to "work around" an issue: perhaps root problem should be solved instead of making "work around"? - When implementing new or updating existing endpoints add/update postman collection for easier local testing.

## Error Handling
Does the code make use of exception handling? Exception handling should be consistent throughout the system.

Does the code simply catch exceptions and log them? Code should handle exceptions, not just log them.

Make sure that most specific exception is catched / throwed in each particular case.
Define and create custom Exception sub-classes to match your specific exception conditions. Exception should be self-describable. If exception class name/message does not help to understand the real problem - it should be changed.

Does the code test all error conditions of a method call?

Make sure the Unit test covers all possible values.

Invalid parameter values are handled properly early in methods (Fast Fail).

Consider using a general error handler to handle known error conditions.

Avoid usage of exceptions to drive some business logic. Exception-driven code is a bad practice.

Does some method returns null? null results are considered to be a bad practice.

Does the code correctly impose conditions for "expected" values? For instance, if a method returns null, does the code check for null?

## Security
Does the code appear to pose a security concern?

Passwords and PII should not be stored in the code base.

User passwords should not be stored or logged anywhere. Even in-memory variables should not keep user password longer than required.

Connect to other systems securely, i.e., use https instead of http where possible.

## Thread Safeness
Does the code practice thread safeness?

If objects can be accessed by multiple threads at one time, code altering global variables (static variables) should be enclosed using a synchronization mechanism.

In general, controllers/servlets should not use static variables.

Use synchronization on the smallest unit of code possible. Using synchronization can cause a huge performance penalty, so you should limit its scope by synchronizing only the code that needs to be thread safe.

Write access to static variable should be synchronized, but not read access.

Even if servlets/controllers are thread-safe, multiple threads can access HttpSession attributes at the same time, so be careful when writing to the session.

Use the volatile keyword to warn that compiler that threads may change an instance or class variable — tells compiler not to cache values in register.

Release locks in the order they were obtained to avoid deadlock scenarios.

Does the code avoid deadlocks?

Avoid calling synchronized methods within synchronized methods.

Locks must be acquired and released in the right order to prevent deadlocks, even in error handling code.

## Resource Leaks
Does the code release resources? Close files, database connections, http connections, etc. Starting from Java 7 use the try-with-resources Statement

Does the code release resources more than once? This will sometimes cause an exception to be thrown.

Does the code use the most efficient class when dealing with certain resources? For instance, buffered input/output classes.

## Control Structures
Does the code make use of infinite loops? If so, please be sure that the end condition can and will be met.

Does the loop iterate the correct number of times? Check initialization and end condition to make sure that the loop will be executed the correct number of times.

## Re-usability
Are all available libraries being used effectively?

Are available application util methods known and used (to avoid code duplication)?

Is the code as generalized as it could be?

Abstract classes makes code tightly coupled and should not be used, only if absolutely necessary. Inheritance should be replaced with composition as a more flexible and testable approach.

Is the code a candidate for re-usability? If you see the same code being written more than once (or if you have copied-and-pasted code from another class), then this code is a candidate.

Hardcoded values (e.g. downstream provider name etc) should be avoided. Instead those values should be extracted as configuration properties. Default value can be used in code and easily overwritten when necessary.

Do not mix approaches with @Value and property configuration class.

## Performance
Objects are duplicated only when necessary.

No busy-wait loops instead of proper thread synchronization methods.

Avoid large objects in memory or using String to hold large documents which should be handled with better tools. For example, don't read a large XML document into a String, or DOM.

Be careful with logging. Sometimes it can cause performance troubles.

Make sure that amount of slow or "heavy" operations is minimized in business logic.

Make sure that huge amounts of data are processed in batches.

Optimization that makes code harder to read should only be implemented if a profiler or other tool has indicated that the routine stands to gain from optimization. These kinds of optimizations should be well documented and code that performs the same task should be preserved.

## Logging
Overall amount of logging in code should be reasonable. Too much logs or logging inside loops could cause performance problems. At the same time, some key events in the system should be transparent.

Make sure that log level is chosen correctly for particular cases: ALL < TRACE < DEBUG < INFO < WARN < ERROR < FATAL

** ERROR - Showstoppers, any kind of issue that results in the termination of a process on an exception state and or is unrecoverable. Eg: Database connection issues, Infrastructure problems, external resources unavailable.

** WARNING - Issues that might impact the application but does not call the system or a process to stop or that the system is programmed to work around. Eg: Automatic updates fail where a recovery strategy is defined, Using default values for something that should have been configured.

** INFO - This level is used to mark major changes in the state of a process or the system. Eg: Cronjob or other automatic process start/ends normally, a new configuration is activated, before and after calling a web service.

** DEBUG - Level used to provide diagnostic information for the developers. On major state changes of the application. Eg: Whenever a business rule causes a change in the flow of the application (if/else/case/for/while), Whenever reaching external resources such as web services.

** TRACE - Cover any changes on objects that might require investigation whenever Java Debug is not an option (Production environment). Should be used to show the granular information about objects and attributes. Eg: Before and after any complex process that modifies any information.

Make sure that building of log message is not expensive for the application. For example, it is a bad idea to load additional data or call some additional methods just for logging purposes.

Make sure that usage of conditions like LOG.isDebugEnabled() are not excess. There is no need to check it if you are logging just a message.

Make sure that creation of log entries are safe. It means that production code should never fail on logging lines.

Make sure that no sensitive information is logged

## Checklist
[ ] Code adheres to the repository's coding guidelines.
[ ] All tests pass with sufficient coverage.
[ ] No hardcoded values or sensitive data in the code.
[ ] Proper error handling and logging are implemented.
[ ] Code is modular and follows the single responsibility principle.