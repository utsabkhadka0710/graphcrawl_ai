# Contributing to GraphCrawl AI

Thank you for considering contributing to GraphCrawl AI.

This project is intentionally beginner-friendly. You do not need years of experience to contribute.

## Ways to Contribute

### Documentation

Examples:

* Fix typos
* Improve README
* Add usage examples
* Improve setup instructions

Great for first-time contributors.

### Testing

Examples:

* Add unit tests
* Improve coverage
* Reproduce bugs

### Bug Fixes

Examples:

* Validation issues
* Error handling improvements
* Logging improvements

### Features

Examples:

* Async crawling
* New extraction modes
* Additional LLM providers
* Better content cleaning

## Getting Started

### 1. Fork the Repository

Click Fork on GitHub.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/graphcrawl_ai.git

cd graphcrawl_ai
```

### 3. Create a Branch

```bash
git checkout -b feature/my-feature
```

### 4. Make Changes

Implement your fix or feature.

### 5. Test Your Changes

Run all tests before opening a pull request.

### 6. Open a Pull Request

Describe:

* What you changed
* Why you changed it
* Any limitations or tradeoffs

## Coding Guidelines

### Keep Functions Small

Prefer:

```python
def clean_content():
    pass

def validate_content():
    pass
```

over huge functions that do many things.

### Use Meaningful Names

Good:

```python
fetch_page_content()
```

Bad:

```python
do_stuff()
```

### Add Type Hints

Whenever possible:

```python
def crawl_url(url: str) -> dict:
```

### Use Pydantic Models

For structured requests and responses.

### Handle Errors Explicitly

Prefer:

```python
try:
    ...
except Exception as e:
    ...
```

over silent failures.

## First Issues

Good beginner contributions include:

* Documentation improvements
* Logging improvements
* Test coverage
* Error messages
* Validation enhancements

## Discussion

If you're unsure where to start:

* Open an issue
* Ask a question
* Suggest an idea

Discussion is encouraged.

## Code of Conduct

Be respectful.

Everyone starts somewhere.

Constructive feedback is welcome.
Personal attacks are not.

Let's build something useful together.
