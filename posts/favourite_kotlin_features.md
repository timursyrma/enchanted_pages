---
title: Favorite Kotlin Features
date: 2025-01-23  
author: S1mY  
---

I decided to talk about the Kotlin features that I actively use and find useful.

## Idioms as a Style of Programming
When it comes to a programming language, it’s hard to evaluate a good language by a single feature. The language's capabilities are closely intertwined, forming a programming style. Their combination shapes what are known as the language's idioms—small recipes for solving typical tasks. They simplify code and make it readable and understandable for other developers.

A good example of this approach in Kotlin is the official [Idioms page](https://kotlinlang.org/docs/idioms.html). We strive to expand these idioms, especially for those coming from Java, to show how familiar tasks can be approached in a new style.

## Documentation and Comparison with Java
Kotlin aims to be an evolution of Java, improving its weaker aspects. The [Comparison to Java](https://kotlinlang.org/docs/comparison-to-java.html) page describes both new features and the pain points that Kotlin addresses. In this article, I’ve decided to focus on the features that Java doesn’t have, but which are widely used in Kotlin.

Of course, this list is by no means complete. You can find more examples and details in the documentation, but I’ve highlighted the features I find most important.

## Obvious and Not So Obvious: First-Class Functions in Kotlin
Functions are a basic concept found in all programming languages. However, from the perspective of a Java developer, using them in Kotlin can look a bit unusual. First-class functions have several interesting characteristics that significantly affect how code is written and organized.

### Freedom from Classes
In Kotlin, you don’t have to attach functions to classes. This is convenient, especially for beginners just learning the language. They don’t need to understand the concepts of classes, interfaces, static methods, or conventions like `public static void main`. They can just start writing code:

```kotlin
fun main() {
    doSomething()
}

fun doSomething() {
    doMoreStuff(::finishWork)
}

fun doMoreStuff(callback: () -> Unit) {
    callback()
}

fun finishWork() {
    TODO("Not implemented yet")
}
```

Here, functions are used as standalone entities, making the code concise and easy to read.

### Grouping by Files Instead of Classes
Using first-class functions changes the approach to project structure. Instead of grouping logic by classes, as is common in Java, you can group it by files. This allows you to create more compact structures, especially when classes with their annotations or complex relationships aren’t needed.

### Classic Java Project Structure
Classes are grouped into separate files and packages:

```
src/
├── controllers/
│   ├── ClientController.java
│   ├── OrdersController.java
├── entities/
│   ├── Client.java
│   ├── Order.java
├── utils/
│   ├── StringUtils.java
```

### Kotlin Project Structure
When using first-class functions, you can simplify the project:

```
src/
├── main.kt
├── controllers.kt
├── entities.kt
├── utils.kt
```

As a result, first-class functions in Kotlin help not only in writing less code but also in structuring programs differently. They allow you to focus on logic and reduce the “noise” of extra classes. Thanks to this:

- Projects become more compact.
- The code is easier to grasp.
- The project structure becomes more tangible.

## Extension Functions: Adding Functionality Without Modifying Classes
One of the powerful features of Kotlin is **extension functions**. They allow you to add behavior to existing classes—even if those classes come from external libraries or other modules where you don’t have the ability to make changes.

### Example: Adding a Function for Data Output
Suppose we have a simple `Client` class with three fields:

```kotlin
class Client(val name: String, val company: String, val twitter: String)

println(Client("Steve", "JetBrains", "@steveminecraft"))
> Client@3ac3fd8b
```

If we try to print an instance of this class to the console, we’ll get a reference to the object, which is obviously not very informative. In Java, a common approach would be to create a helper class with a method that accepts an object and formats its data.

### Approach with an Extension Function
Instead, in Kotlin, you can add an extension function:

```kotlin
fun Client.toConsole() =
    "Client[name=${name}, ${company}, ${twitter}]"

println(Client("Steve", "JetBrains", "@steveminecraft").toConsole())
> Client[name=Steve, JetBrains, @steveminecraft]
```

Here:
1. `toConsole` is an extension function added to the `Client` class.  
2. Inside the function, you can access the class fields as if it were its method.  
3. This significantly simplifies working with types, making the code cleaner and shorter.

### Alternative: External Function
If for some reason you don’t want to use an extension function, you can implement similar functionality with a regular function:

```kotlin
fun toConsole(client: Client) =
    "Client[name=${client.name}, ${client.company}, ${client.twitter}]"

println(toConsole(Client("Steve", "JetBrains", "@steveminecraft")))
> Client[name=Steve, JetBrains, @steveminecraft]
```

However, in this case the syntax becomes a bit more verbose, as you have to explicitly specify the `client` object.

### Working with Types Not Under Your Control
A key advantage of extension functions is the ability to add behavior to types that you cannot modify—for example, classes from third-party libraries. This is especially useful when you need to adapt types to your needs without touching the original code.

In summary, extension functions:
- Simplify adding logic to existing types.
- Make code more concise by providing direct access to the object’s fields.
- Help adapt third-party classes without modifying them.
- Are particularly useful for creating domain-specific languages (DSL), where minimizing code “noise” and staying within a very simple syntax is important.

### Extension Functions in Framework Integration: Example with Spring
One of Kotlin’s key advantages is the ability to write extension functions for classes from third-party libraries. This is especially helpful when you use popular frameworks like Spring and want to improve the readability and convenience of their APIs.

### Example with Spring and JDBC Template
Let’s say we’re running an SQL query using `JdbcTemplate` from the Spring Framework. Standard code in Java looks something like this:

```java
@Override
public <T> List<T> query(String sql, RowMapper<T> rowMapper, @Nullable Object... args) throws DataAccessException {
    return result(query(sql, args, new RowMapperResultSetExtractor<>(rowMapper)));
}
```

We need to pass:
- The SQL query
- A mapper (for example, an implementation of `RowMapper`)
- Parameters for the SQL
- A readability challenge

When the SQL query and mapper become large, parameters end up being “scattered” in the code. For example:

```kotlin
fun findMessageById(id: String) = db.query(
    """
    select * from messages where id = ?
    and ... (very long query)
    """,
    RowMapper { rs, _ ->
        Message(rs.getString("id"), rs.getString("text"), rs.getString("xxxxx"))
    },
    id
)
```

Here:
- The `id` parameter is far from the actual SQL query.
- The mapper takes up a lot of space, distracting from the main logic.

### Solution: Extension Functions and Trailing Lambda
In Kotlin, you can solve this readability problem by using an extension function for `JdbcOperations` that changes the order of parameters:

```kotlin
fun findMessageById(id: String) = db.query(
    "select * from messages where id = ?", 
    id
) { rs, _ ->
    Message(rs.getString("id"), rs.getString("text"))
}
```

### Benefits
- **More readable code**: The SQL query and its parameters are now adjacent.  
- **Trailing lambda**: The mapper is placed outside the parentheses, making the method call more concise.

### How It Works
The `query` function from Spring has been supplemented by an extension function that changes the parameter order. As a result, the call becomes more convenient for Kotlin developers. This is an example of how popular frameworks adapt their APIs for Kotlin to improve readability and convenience.

### Lambda Conversion
Methods in Java that accept interfaces with a single method (Single Abstract Method) are automatically converted into lambdas in Kotlin, making the calls even shorter.

### Usage in Other Libraries
If you work directly with JDBC (without Spring) or with other libraries, you can create your own extension functions. For example:

```kotlin
fun Connection.query(sql: String, params: List<Any>, mapper: (ResultSet) -> T): List<T> {
    // Implementation
}
```

This allows you to adapt the code to your needs, creating a convenient API even for basic tools.

### Are Extension Functions Available via Reflection API?
**Answer:**  
Yes, extension functions are accessible through the Reflection API. They are resolved as static methods, and you can call them if you know their name. This is because extension functions are actually compiled into static methods, which take the extended type's object as the first parameter.

### How to Test Extension Functions?
**Answer:**  
Because extension functions are static methods, testing them can be tricky if you want to use mocks. However, the [Mockito Kotlin](https://github.com/mockito/mockito-kotlin) library provides utilities for working with such functions. You can mock and test extension functions just like any other static methods.

### Are Extension Functions Inherited by Descendants?
**Answer:**  
No, extension functions are not inherited. They are statically resolved in the context of the type they extend. This is because extension functions do not modify the original class but add extra behavior at compile time.

**Example:**

```kotlin
open class Parent
class Child : Parent()

fun Parent.extensionFunction() = println("Extension on Parent")

fun main() {
    val child: Parent = Child()
    child.extensionFunction() // Output: "Extension on Parent", not "Child"
}
```

Thus, they behave like regular static methods and are not subject to dynamic polymorphism.

### Conclusion
- They improve code readability.
- They allow you to adapt third-party libraries.
- They’re ideal for working with frameworks like Spring, making the code concise and idiomatic.

## Contextual Functions in Kotlin: Simplifying Working with Objects
Kotlin offers a rich set of contextual functions in its standard library, such as `apply`, `also`, `let`, `run`, and `with`. These functions are commonly used to work with objects in local contexts, simplifying and making code more concise.

The [Scope Functions documentation](https://kotlinlang.org/docs/scope-functions.html) explains them in detail. Here, I’ll provide a few examples to show their usage.

### apply for Object Configuration
A classic example is configuring an object. In Java, this often looks cumbersome because you have to set each attribute with a separate call. In Kotlin, you can do it compactly with `apply`.

**Before:**

```kotlin
val dataSource = BasicDataSource()
dataSource.driverClassName = "com.mysql.jdbc.Driver"
dataSource.url = "jdbc:mysql://domain:3309/db"
dataSource.username = "username"
dataSource.password = "password"
dataSource.maxTotal = 40
dataSource.maxIdle = 40
dataSource.minIdle = 4
```

**Using apply:**

```kotlin
val dataSource = BasicDataSource().apply {
    driverClassName = "com.mysql.jdbc.Driver"
    url = "jdbc:mysql://domain:3309/db"
    username = "username"
    password = "password"
    maxTotal = 40
    maxIdle = 40
    minIdle = 4
}
```

**How It Works:**
1. `apply` is an extension function on any type.
2. It takes a lambda with a receiver, which is bound to the object.
3. The code in the block executes in the context of the object, and the function returns that object (`this`).

### let for Working with Nullable Objects
`let` is commonly used for null checks and performing actions on an object.

**Before:**

```kotlin
val order = retrieveOrder()
if (order != null) {
    processCustomer(order.customer)
}
```

**Using let:**

```kotlin
retrieveOrder()?.let {
    processCustomer(it.customer)
}
```

**Advantages:**
- Reduces the number of temporary variables.
- Code is more compact and readable.

### Problem of Choice: Which Function to Use?
Scope functions often look similar, which can be confusing. Here’s a brief table for reference:

| Function | Object Reference | Return Value       | Is Extension |
|----------|------------------|--------------------|-------------|
| let      | it              | Lambda result      | Yes         |
| run      | this            | Lambda result      | Yes         |
| with     | this            | Lambda result      | No          |
| apply    | this            | Context object     | Yes         |
| also     | it              | Context object     | Yes         |

**Selection Rule:**  
- If you need to return the object itself, use `apply` or `also`.  
- If you need to return the result of the block, use `let`, `run`, or `with`.

### Implementation Details
1. All scope functions in Kotlin are implemented as extension functions. This allows you to call them on any object.
2. Many context functions use lambdas with receivers. This special syntax lets you refer to the object inside the lambda directly via `this`.

## Default Parameter Values and Named Parameters
Kotlin provides powerful features to simplify working with functions and constructors: default parameter values and named parameters. These features reduce boilerplate code and improve readability, especially when dealing with many arguments.

In Java, you often use method overloading to handle default parameter values. In Kotlin, you can just specify them in the function declaration.

**Example: Before**

```kotlin
fun find(name: String) {
    find(name, true)
}

fun find(name: String, recursive: Boolean) {
    // Implementation
}
```

**Example: After**

```kotlin
fun find(name: String, recursive: Boolean = true) {
    // Implementation
}

fun main() {
    find("myfile.txt") // Called with recursive = true
}
```

**Benefits:**
1. Less code: No need to create multiple overloaded methods.  
2. Simpler calls: You can specify only the parameters that matter in your situation.

### Named Parameters
When a function or constructor has many parameters, it can be hard to tell which argument corresponds to which parameter. Named parameters solve this by letting you explicitly specify which value goes to which parameter.

### Example: Compile Error Without Named Parameters

```kotlin
class Figure(
    val width: Int = 1,
    val height: Int = 1,
    val depth: Int = 1,
    val color: Color = Color.BLACK,
    val description: String = "This is a 3D figure"
)

Figure(Color.RED, "Red figure") // Compilation error
```

Here, Kotlin doesn’t know which constructor parameters `Color.RED` and `"Red figure"` refer to.

### Solution: Named Parameters

```kotlin
Figure(color = Color.RED, description = "Red figure")
```

**Benefits:**
1. Clarity: Instead of remembering parameter order, you explicitly specify which parameter receives which value.  
2. Flexibility: You can pass only the parameters you need, ignoring the others.  
3. Readability in code reviews: Unlike IDE hints, which are not visible in code reviews, named parameters are always clear.

## Expressions in Kotlin: Compact and Expressive Code
One of Kotlin’s strengths is the ability to use constructs like `if`, `when`, and even `try` as expressions that return a value. This makes code more compact and elegant.

### Example: if as an Expression
In Java, `if` is always a statement, requiring you to assign a value to a variable inside a block. In Kotlin, `if` can be an expression that returns a value.

**Before (Java-style):**

```kotlin
fun adjustSpeed(weather: Weather): Drive {
    val result: Drive
    if (weather is Rainy) {
        result = Safe()
    } else {
        result = Calm()
    }
    return result
}
```

**After (Kotlin):**

```kotlin
fun adjustSpeed(weather: Weather): Drive {
    val result = if (weather is Rainy) {
        Safe()
    } else {
        Calm()
    }
    return result
}
```

Or even shorter:

```kotlin
fun adjustSpeed(weather: Weather): Drive =
    if (weather is Rainy) Safe() else Calm()
```

**Benefits:**
1. Less code: No extra temporary variables.  
2. Clarity: It’s immediately clear which value is returned for each condition.

### Example: when as an Expression
When there are more conditions, use `when`, which replaces nested `if-else`.

**Example with sealed classes:**

```kotlin
sealed class Weather
class Sunny : Weather()
class Rainy : Weather()

fun adjustSpeed(weather: Weather): Drive = when (weather) {
    is Rainy -> Safe()
    is Sunny -> Calm()
}
```

**Features:**
- The compiler checks that all possible variants of the sealed class are covered.  
- If there are unhandled branches, it results in an error or warning, depending on the settings.

### New in Kotlin 1.5.30: Sealed when
Kotlin 1.5.30 added strict branch coverage for `when`, even when used as a statement (not just as an expression). This is useful for preventing unhandled new class variants.

**Balancing Strictness and Flexibility**  
If you add an `else` branch, `when` covers all cases, including any future ones you might add. This is convenient but risky: a newly added type might be overlooked.  
Some companies use static code analysis to prohibit using `else` in `when` statements for sealed classes. This helps avoid errors by requiring explicit handling of all cases.

## Functional Types and Their Extension in Kotlin
Kotlin provides powerful tools for working with functions, including the use of functional types and their inheritance. These features make code more expressive and extensible, especially in scenarios involving frameworks or complex logic.

Functional types are types describing functions. For example, `() -> T` represents a function that takes no arguments and returns a value of type `T`.

### Example: Using a Functional Type

```kotlin
fun <T> someFunction(function: () -> T): T {
    return function()
}

fun someOtherFunction() {
    val s: String = someFunction { "Hello" }
}
```

In this example:
1. `someFunction` takes a parameter of type `() -> T` (a function that takes no arguments and returns `T`).  
2. The lambda `{ "Hello" }` is passed as an argument, and its result (`"Hello"`) is used as the return value.

### Typealiases for Convenience
When functional types are used frequently, you can simplify them with `typealias`.

**Example: Defining typealias**

```kotlin
typealias Action<T> = () -> T

fun <T> someFunction(function: Action<T>): T {
    return function()
}
```

Using `typealias` makes the code cleaner and easier to understand, especially if the functional types are more complex or verbose.

### Inheritance from Functional Types
Kotlin allows you to inherit from functional types, enabling new possibilities.

**Example: Inheriting from a Functional Type**

```kotlin
typealias Action<T> = () -> T

class MyAction<T>(val param: String) : Action<T> {
    override fun invoke(): T {
        TODO("Not yet implemented")
    }
}

fun <T> someFunction(function: Action<T>): T {
    return function()
}

fun someOtherFunction() {
    val s: String = someFunction(MyAction("Greetings"))
}
```

**Why Do We Need This?**
1. **Extending the functional type**: You can add parameters via the constructor (like `param` in the example).  
2. **Integration with frameworks**: In some frameworks, handlers (e.g., for requests) are represented as functional types. Inheriting lets you add extra parameters or behavior.

### Suspend Functions and Their Inheritance
Starting with Kotlin 1.5.30, you can inherit from `suspend` functional types as well. This is particularly helpful when working with coroutines.

**Example: Suspend Functional Type**

```kotlin
typealias SuspendAction<T> = suspend () -> T

class MySuspendAction<T>(val param: String) : SuspendAction<T> {
    override suspend fun invoke(): T {
        TODO("Not yet implemented")
    }
}
```

## Lambda with Receiver in Kotlin: Basics and Examples
Kotlin has a special concept called **lambda with receiver**. This construct lets you write expressions in the context of a particular object, accessing its properties and methods directly through `this` (without needing to explicitly reference the object).

In the documentation, this is referred to as [Function Literals with Receiver](https://kotlinlang.org/docs/lambdas.html#function-literals-with-receiver).

### apply Function
A lambda with receiver is heavily used in the Kotlin standard library. For example, the `apply` function allows you to execute a block of code in the context of the current object, returning that object:

```kotlin
val dataSource = BasicDataSource().apply {
    driverClassName = "com.mysql.jdbc.Driver"
    url = "jdbc:mysql://domain:3309/db"
    username = "username"
    password = "password"
}
```

- Inside the code block, you’re referencing the properties of `dataSource` directly via `this`, making the code more readable and concise.  
- The result of calling `apply` is the `BasicDataSource` object itself.

### Creating a Function with a Receiver Lambda
If you want to simplify object creation or write domain-specific code, you can define your own function that takes a receiver lambda:

```kotlin
fun dataSource(config: BasicDataSource.() -> Unit): BasicDataSource {
    return BasicDataSource().apply(config)
}

// Usage:
val ds = dataSource {
    driverClassName = "com.mysql.jdbc.Driver"
    url = "jdbc:mysql://domain:3309/db"
    username = "username"
    password = "password"
}
```

Here:
- `BasicDataSource.() -> Unit` is the signature of a lambda with receiver.  
- Inside the `config` block, the `BasicDataSource` object's properties are directly accessible.

### buildString Function
The standard library includes the `buildString` function, which demonstrates the capabilities of lambdas with receivers:

**In Java:**

```java
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 5; i++) {
    sb.append("Hello, ").append("Joe").append("!\n");
}
System.out.println(sb);
```

**In Kotlin with `buildString`:**

```kotlin
val result = buildString {
    repeat(5) {
        append("Hello, ")
        append("Joe")
        appendLine("!")
    }
}
println(result)
```

- `buildString` runs the code block inside a `StringBuilder`.  
- The syntax is concise and easy to read.

## Lambda with Receiver in DSL (Domain-Specific Language)
Kotlin heavily uses lambdas with receivers to build DSLs. Consider the example of the [`kotlinx.html`](https://github.com/Kotlin/kotlinx.html) library for generating HTML:

```kotlin
html {
    body {
        h1 { +"Welcome to Kotlin DSL" }
        ul {
            for (i in 1..5) {
                li { +"Item $i" }
            }
        }
    }
}
```

- Each construct (`html`, `body`, `h1`, `ul`, `li`) is a lambda with receiver.  
- In the context of each lambda, the corresponding HTML tag’s properties and methods are available.

### Lambda with Receiver in Ktor
Lambdas with receivers are also used in the [Ktor](https://ktor.io/) framework for creating DSL routes and handling HTTP requests:

```kotlin
embeddedServer(Netty, port = 8080) {
    routing {
        get("/html-dsl") {
            call.respondHtml {
                body {
                    h1 { +"Ktor HTML DSL" }
                    ul {
                        for (i in 1..10) {
                            li { +"Item $i" }
                        }
                    }
                }
            }
        }
    }
}.start(wait = true)
```

## Kotlin and Null Safety
One of Kotlin’s key features is built-in **Null Safety**, aimed at minimizing errors related to `NullPointerException`. This feature makes life much easier for developers, but it has some nuances, especially when interacting with Java code. Let’s look at the main aspects of null safety and illustrate them with examples.

Kotlin lets you declare types that may or may not hold `null`. This is done using the question mark (`?`). For example:

```kotlin
class Nullable {
    fun someFunction() {}
}

fun createNullable(): Nullable? = null

fun main() {
    val n: Nullable? = createNullable()
    n?.someFunction() // Safe call
}
```

In this example:
- `Nullable?` is a type that allows `null`.  
- `?.` is the **safe call** operator, which invokes a method only when the value is not `null`.

### Problem at the Kotlin-Java Boundary
Despite the elegance of Kotlin’s null safety, it interacts with Java, where `null` is perfectly normal. This leads to “platform types” in Kotlin. They are types coming from Java code where the Kotlin compiler cannot be certain whether `null` is possible.

**Example (Java):**
```java
public static String getNullableValue() {
    return null; // May return null
}
```

**Example (Kotlin):**
```kotlin
val value: String = getNullableValue() // The compiler won’t warn about a potential null!
```

Here, Kotlin “trusts” the Java method, not assuming it could return `null`, which can lead to a `NullPointerException`.

### Solutions for Working with Null
Kotlin provides several tools for handling potentially `null` values:

a. **Safe Call (`?.`)**  
```kotlin
val city = order?.customer?.address?.city
```

b. **Elvis Operator (`?:`)**  
Sets a default value if the variable is `null`:
```kotlin
val name = user?.name ?: "Guest"
```

c. **Not-Null Assertion (`!!`)**  
Forcibly asserts that a value is non-null. Use with caution:
```kotlin
val nonNullValue = nullableValue!! // Can throw NullPointerException!
```

### Not Recommended Usage
```kotlin
private var state: State? = null

@BeforeEach
fun setup() {
    state = State("abc")
}

@Test
fun test() {
    assertEquals("abc", state!!.data) // Avoid this approach
}
```

### Using Delegates
A better solution is to use delegates:
```kotlin
lateinit var state: State
```

### Handling Errors at the API Level
If Java methods return platform types, explicitly declare them as nullable or non-nullable in Kotlin.

### Using Null Safety in DSL and DSL Approach
One reason Kotlin is popular is its ability to create safe DSLs with null checks in mind. For instance:

```kotlin
val html = buildString {
    append("<html>")
    append("<body>")
    append("Hello, Kotlin!")
    append("</body>")
    append("</html>")
}
```

### Java Interoperability
Kotlin provides seamless access to all Java libraries, such as Spring, Hibernate, TestContainers, and many more. However, there are nuances that may require special attention when mixing Kotlin with Java.

**Example with TestContainers**, which uses recursive generics to build a fluent API:

**Java code:**
```java
PostgreSQLContainer<?> container = new PostgreSQLContainer<>("postgres:13")
    .withInitScript("schema.sql")
    .withDatabaseName("database")
    .withUsername("user")
    .withPassword("password");
```

This Java code is straightforward, as each method returns the current container with the correct type.

**Kotlin code (compatibility issue):**
```kotlin
val container: PostgreSQLContainer<*> = PostgreSQLContainer<Nothing>("postgres:13")
    .withInitScript("schema.sql")
    .withDatabaseName("database")
    .withUsername("user")
    .withPassword("password") // Error: method returns Nothing
```

The problem arises because Kotlin interprets the return type as `Nothing`, breaking the method chain.

### Solution via `apply`
Kotlin suggests using `apply` to get around this problem:

```kotlin
val container = PostgreSQLContainer<Nothing>("postgres:13").apply {
    withInitScript("schema.sql")
    withDatabaseName("database")
    withUsername("user")
    withPassword("password")
}
```

Using `apply`, you can configure the container inside a block without relying on each method’s return type to be correct.

## Recursive Generics
Starting with Kotlin 1.5.30, there is experimental support for recursive generics. To use this feature, you must enable the corresponding compiler flag.

```kotlin
// Example usage (experimental feature):
val container: PostgreSQLContainer<*> = PostgreSQLContainer("postgres:13")
    .withInitScript("schema.sql")
    .withDatabaseName("database")
    .withUsername("user")
    .withPassword("password")
```

---

These are some of the features that make Kotlin stand out—first-class functions, extension functions, scope functions, null safety, and more. They combine to create a concise, expressive, and safe environment for development, whether you’re coming from Java or just beginning your journey with the language.
