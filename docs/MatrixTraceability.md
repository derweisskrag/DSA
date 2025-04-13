# Matrix Traceability - PM tool 

Matrix traceability is a special tool in a project manager toolkit. 
It helps you to track all the things in one place to achieve the goal 
of the project.

## Goal of the Project Management

To apply all the skills, knowledge, techniques and tools to achieve the objective
of the project; to ensure successful project delivery within scope, time, and 
budget constraints.

## Why do you need Matrix Traceability? Who cares?

Based on the first impression about the tool, you would find yourself reflecting
on how you approached the risk and error management in your application or a part 
of it (say, the upgrade CRM system discussed in the individual assignment).

### Key advantage

The simplest way of documenting all the requirements, tests, features and other 
deliverables in one place. Please, check out this table:

| Requirement \ Test | Test 1 | Test 2 | Test 3 | ... |
|--------------------|--------|--------|--------|-----|
| Requirement 1      |   X    |        |        |     |
| Requirement 2      |        |   X    |        |     |
| Requirement 3      |        |        |   X    |     |
| Requirement 4      |   X    |   X    |        |     |
| Requirement 5      |        |        |        |  X  |

The pattern follows the pattern where you place all requirements (labelled in a certain way such as requirement 1 or requirement 1.1) 
and tests on columns. The intersection meaning goes beyond failure or acceptance: it denotes that one considers the test for this 
particular requirement. However, you can use "✔️" or "❌" symbols to denote whatever you decide.

## Example of what you can do

### Web Store

The first simple application is the full-stack web application:

1. Requirement 1 - Front-end
2. Requirement 2 - Back-end
3. Requitement 3 - API (Controllers, Services, Entities, Views, Factories => API)
4. Requirement 4 - Authorization
5. Requirement 5 - Performance & Scalability
6. others

For each requirement, one must consider tests and what means "success". They also plan
the entire process of testing and how they educate users (users also help to optimize 
and use the application in the designed way - always an important part of the software):

| Requirement | Test Type | Test Description                               | Status       |
|-------------|-----------|-----------------------------------------------|--------------|
| R1          | T1        | Test responsiveness of homepage across devices | Passed       |
| R2          | T2        | Test API data retrieval for user data          | Pending      |
| R3          | T3        | Test user login with valid and invalid credentials | In Progress |
| R4          | T4        | Test website load time under different conditions | Not Started |

### Working on LinkedList?

It is also possible to consider using the Matrix Traceability tool for managing any part 
of your system or application, say, API designed for working with linked lists:

| **Requirement** | **Test Type** | **Test Description**                                      | **Status**      |
|-----------------|---------------|-----------------------------------------------------------|------------------|
| R1              | Functional    | Test `insert` operation at the head and tail of the list  | Passed          |
| R2              | Functional    | Test `delete` operation from an empty list                | In Progress     |
| R3              | Functional    | Test `search` operation for existing and non-existing nodes | Pending      |
| R4              | Performance   | Measure API response time for `insert` in large lists     | Not Started     |
| R5              | Boundary      | Test `insert` operation with invalid index (e.g., -1)     | Passed          |
| R6              | Functional    | Test `traverse` operation to retrieve all list elements   | Passed          |
| R7              | Error Handling| Verify error handling for null pointer dereference        | In Progress     |
| R8              | Performance   | Test API load time for handling large data sets           | Pending         |
| R9              | Security      | Test authorization for access to linked list API endpoints | Not Started   |
| R10             | Integration   | Ensure linked list API integrates with other data endpoints | Pending     |

## Tests

According to Rust, there are two types of tests: 

1. Unittests
2. Integration tests
3. Others

### Example: Unittest

```rs
fn add(x: i32, y: i32) -> i32 {
    x + y
}

#[cfg(test)]
mod test {
    use super::*;
    
    #[test]
    fn test_add(){
        assert_eq!(add(2, 2), 4);
    }
}
```

NB! All the code in one file: `main.rs`.

### Example: Integration

```rs
use try_rust::week_2::mosquitoes_lab::{Larva, Gender, Mosquito};


pub mod test_addition {
	use super::*;

	#[test]
	pub fn test_example(){
		
		let a: i32 = 2;
		let b: i32 = 4;
		assert_eq!(a + b, 6);
	}

	#[test]
	pub fn test_larva(){
		let larvae: Vec<Larva> = vec![
			Larva { dna: "ModifiedDNA".to_string(), gender: Gender::Male },
			Larva { dna: "ModifiedDNA".to_string(), gender: Gender::Female },
			Larva { dna: "ModifiedDNA".to_string(), gender: Gender::Female }
		];

		let (males, females) = Mosquito::split_larvae_by_gender(larvae);
		assert_eq!(males.len(), 1);
		assert_eq!(females.len(), 2);
	}
}  
```

NB! All the code is separated, and the built version is in `src/lib.rs`, 
while tests are in `tests/week2/mod.rs`. Simple tests can also be placed
in `tests/random_test.rs`. Rust also recognized the documentation test.

### Did you spot the difference?

It turns out that the integration tests are trying to access your built code.
It means that you test how the different parts of a system work together. The
unit test, however, tests the functionality alone. 

It means that when you want to test your C# Desktop application, you handle 
unit tests and integration tests. 

#### Little example: factorial

Consider the code:

```cs
 [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public long factorial(int value)
        {
            if (this.isBasicCase(value)) return 1;


            if (this._cache.ContainsKey(value)) return this._cache[value];

            long result = value * this.factorial(value - 1);
            this._cache[value] = result;
            return result;
        }
```

The simplest way to test it is by using unit testing (in the src directory). However, when
you want to test the appliaction entirely, you should consider deploying some part of your
app as library (in Rust: `lib.rs`), and then importing it in `tests/your_test/type/test.cs`


## Conclusion

Traceability Matrix is special tool that opens new possibilities for you. Now you reflect on 
your app more than just tests. You consider the requirements, users, stakeholders, etc. In other
words:

> **Ensure successful project delivery within scope, time, and budget constraints.**



















