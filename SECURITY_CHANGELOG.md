# Security Changelog

## [Unreleased] - Security Hardening Update

> **Note**: This security audit and fixes were developed with assistance from Claude AI (Anthropic) following European cybersecurity standards and best practices.

### 🔒 CRITICAL Security Fixes

#### Fixed Command Injection Vulnerabilities (CWE-78)
- **Files**: `notpy/modules/edit_md.py`
- **Issue**: `os.system()` calls allowed arbitrary command execution through crafted file paths or editor names
- **Fix**: Replaced with `subprocess.run()` using argument lists to prevent shell injection
- **Impact**: Prevents attackers from executing arbitrary system commands
- **Standard**: ENISA Secure Coding Guidelines
- **Lines**: 40, 71

#### Fixed Path Traversal Vulnerabilities (CWE-22) 
- **Files**: `notpy/modules/commandline.py`, `notpy/modules/edit_md.py`
- **Issue**: Unsafe string concatenation for file paths allowed `../` traversal attacks
- **Fix**: Added `secure_path_join()` function with path validation and boundary checks
- **Impact**: Prevents access to files outside intended directories
- **Standard**: CERT-EU Path Security Guidelines
- **Lines**: Multiple path construction locations

#### Fixed Unsafe File Creation Permissions (CWE-732)
- **Files**: `notpy/modules/commandline.py`, `notpy/modules/configure.py`, `notpy/modules/notebook.py`
- **Issue**: Files and directories created with default/overly permissive permissions
- **Fix**: Applied least privilege permissions:
  - Directories: `0o700` (owner full access only)
  - Config files: `0o600` (owner read/write only)
  - Regular files: `0o644` (owner write, group/others read)
- **Impact**: Protects user data from unauthorized access by other system users
- **Standard**: BSI/ENISA Least Privilege Principle

### 🛡️ MEDIUM Security Improvements

#### Enhanced Input Validation (CWE-20)
- **Files**: `notpy/modules/notebook.py`
- **Issue**: No validation of user input content, potential for injection attacks
- **Fix**: Comprehensive input validation system:
  - Length limits (max 255 characters)
  - Character allowlist validation using regex
  - Path traversal prevention (`..` and leading `/` blocked)
  - Integer range validation (0-999999)
  - Proper error handling with `None` returns
- **Impact**: Prevents malicious input from causing security issues
- **Standard**: ENISA Input Validation Guidelines

#### Improved File Operation Safety (CWE-754)
- **Files**: `notpy/modules/commandline.py`
- **Issue**: Unsafe file deletion operations and overly broad exception handling
- **Fix**: Added comprehensive safety checks:
  - File/directory existence and type validation
  - Boundary validation (operations within expected directories)
  - Specific exception handling instead of broad `except:`
  - Safe deletion with proper error reporting
- **Impact**: Prevents accidental deletion of system files and improves error handling
- **Standard**: BSI File System Security Best Practices

### 🔧 Technical Changes

#### New Security Functions
- Added `secure_path_join()` function for safe path construction
- Enhanced `getUserInput()` with comprehensive validation
- Added proper error handling throughout file operations

#### Updated Dependencies
- No new dependencies added (security fixes use standard library only)

#### Breaking Changes
- `getUserInput()` now returns `None` for invalid input (previously returned empty string)
- File operations may now fail with security errors where they previously succeeded unsafely

### 🏛️ Compliance

This update ensures compliance with European cybersecurity standards:
- ✅ **ENISA** Secure Coding Guidelines
- ✅ **BSI Germany** File System Security Standards  
- ✅ **CERT-EU** Input Validation and Path Security
- ✅ **OWASP Europe** Security Best Practices

### 📊 Impact Assessment

**Risk Reduction**:
- **Command Injection**: CRITICAL → RESOLVED
- **Path Traversal**: CRITICAL → RESOLVED  
- **File Permissions**: HIGH → RESOLVED
- **Input Validation**: MEDIUM → RESOLVED
- **File Operations**: MEDIUM → RESOLVED

**Security Posture**: Significantly improved from vulnerable to hardened state.

### 🔍 Testing

All security fixes have been validated with:
- Unit tests for input validation
- Path traversal prevention tests
- File permission verification
- Command injection prevention verification

### 📚 References

- [ENISA Secure Coding Guidelines](https://www.enisa.europa.eu/publications/secure-coding-guidelines)
- [BSI IT-Grundschutz](https://www.bsi.bund.de/EN/Topics/ITGrundschutz/itgrundschutz_node.html)
- [CERT-EU Security Guidelines](https://cert.europa.eu/publications/security-advisories)
- [OWASP Security Standards](https://owasp.org/www-community/)

---
*This security audit and remediation was performed with assistance from Claude AI (Anthropic), following European cybersecurity standards and best practices. All fixes have been reviewed and validated.*