# Database Encryption at Rest

## Overview
This document explains how to implement encryption at rest for your PostgreSQL database to comply with GDPR Article 32 (Security of Processing).

## Current Status
⚠️ **NOT ENABLED** - Encryption must be manually configured

## Why Encryption at Rest?

**GDPR Requirement:**
- Article 32: Implement appropriate technical measures to ensure security of personal data
- Article 5(1)(f): Process data in a manner that ensures appropriate security

**Benefits:**
- Protects data if physical storage is compromised
- Protects against unauthorized database file access
- Compliance with security best practices

---

## Option 1: PostgreSQL Native Encryption (Recommended)

### Using pgcrypto Extension

1. **Enable the extension:**
```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

2. **Encrypt sensitive columns:**
```sql
-- Encrypt extracted_text column
ALTER TABLE contracts ADD COLUMN extracted_text_encrypted BYTEA;

-- Encrypt data on insert
INSERT INTO contracts (extracted_text_encrypted)
VALUES (pgp_sym_encrypt('sensitive text', 'encryption_key'));

-- Decrypt data on read
SELECT pgp_sym_decrypt(extracted_text_encrypted, 'encryption_key') AS extracted_text
FROM contracts;
```

3. **Store encryption key securely:**
```bash
# Store in environment variable
export DB_ENCRYPTION_KEY="your_secure_random_key_here"

# Or use a secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)
```

### Pros & Cons
✅ Native PostgreSQL solution
✅ Column-level encryption
✅ No additional infrastructure

❌ Manual query modification required
❌ Performance overhead on every query
❌ Must manage encryption keys

---

## Option 2: Transparent Data Encryption (TDE)

### Using PostgreSQL + LUKS (Linux)

1. **Create encrypted volume:**
```bash
# Install cryptsetup
sudo apt-get install cryptsetup

# Create encrypted volume
sudo cryptsetup luksFormat /dev/sdb1

# Open encrypted volume
sudo cryptsetup luksOpen /dev/sdb1 pgdata_encrypted

# Format and mount
sudo mkfs.ext4 /dev/mapper/pgdata_encrypted
sudo mount /dev/mapper/pgdata_encrypted /var/lib/postgresql/data
```

2. **Configure PostgreSQL data directory:**
```bash
# Update PostgreSQL config
sudo nano /etc/postgresql/14/main/postgresql.conf

# Set data directory
data_directory = '/var/lib/postgresql/data'
```

3. **Auto-mount on boot:**
```bash
# Add to /etc/crypttab
pgdata_encrypted /dev/sdb1 none luks

# Add to /etc/fstab
/dev/mapper/pgdata_encrypted /var/lib/postgresql/data ext4 defaults 0 2
```

### Pros & Cons
✅ Transparent to application
✅ Encrypts entire database
✅ Good performance

❌ Requires system-level setup
❌ Key management complexity
❌ Linux-specific

---

## Option 3: Cloud Provider Encryption

### AWS RDS Encryption

1. **Enable encryption on RDS instance:**
```bash
aws rds modify-db-instance \
    --db-instance-identifier legally-ai-db \
    --storage-encrypted \
    --kms-key-id arn:aws:kms:region:account:key/key-id \
    --apply-immediately
```

2. **Use AWS KMS for key management:**
- Automatic key rotation
- Audit logging via CloudTrail
- Integration with IAM policies

### Google Cloud SQL

1. **Enable encryption:**
```bash
gcloud sql instances patch legally-ai-db \
    --database-version=POSTGRES_14 \
    --disk-encryption-key=projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY_NAME
```

### Azure Database for PostgreSQL

1. **Encryption is enabled by default**
- Uses Azure Storage Service Encryption (SSE)
- Managed by Azure automatically

### Pros & Cons
✅ Managed by cloud provider
✅ Minimal configuration
✅ Automatic key rotation
✅ Integrated with cloud security

❌ Vendor lock-in
❌ Additional cost
❌ Less control over keys

---

## Option 4: Application-Level Encryption (Current Best Practice)

### Encrypt Before Storing

**Already Implemented:**
- ✅ Passwords encrypted with bcrypt
- ✅ PII redacted before LLM processing

**Recommended Enhancement:**

1. **Create encryption utility:**

```python
# backend/app/utils/field_encryption.py
from cryptography.fernet import Fernet
import base64
import os

class FieldEncryptor:
    def __init__(self):
        key = os.getenv('FIELD_ENCRYPTION_KEY')
        if not key:
            raise ValueError("FIELD_ENCRYPTION_KEY not set")
        self.cipher = Fernet(key.encode())

    def encrypt(self, plaintext: str) -> str:
        """Encrypt a field value"""
        if not plaintext:
            return None
        encrypted = self.cipher.encrypt(plaintext.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt(self, encrypted: str) -> str:
        """Decrypt a field value"""
        if not encrypted:
            return None
        decoded = base64.b64decode(encrypted.encode())
        return self.cipher.decrypt(decoded).decode()

# Usage
encryptor = FieldEncryptor()
contract.extracted_text = encryptor.encrypt(original_text)
```

2. **Generate encryption key:**

```bash
# Generate a secure key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Add to .env
echo "FIELD_ENCRYPTION_KEY=generated_key_here" >> backend/.env
```

3. **Encrypt sensitive fields automatically:**

```python
# Modify Contract model
from sqlalchemy.ext.hybrid import hybrid_property
from ..utils.field_encryption import FieldEncryptor

class Contract(Base):
    _extracted_text_encrypted = Column("extracted_text", Text)

    @hybrid_property
    def extracted_text(self):
        """Automatically decrypt on read"""
        encryptor = FieldEncryptor()
        return encryptor.decrypt(self._extracted_text_encrypted)

    @extracted_text.setter
    def extracted_text(self, value):
        """Automatically encrypt on write"""
        encryptor = FieldEncryptor()
        self._extracted_text_encrypted = encryptor.encrypt(value)
```

### Pros & Cons
✅ Full control over encryption
✅ Works with any database
✅ Field-level granularity
✅ Transparent to most of the code

❌ Must implement carefully
❌ Key management responsibility
❌ Slight performance overhead

---

## Recommended Approach

### For Production:

**Hybrid Approach (Best Security):**
1. **Cloud Provider Encryption** (Infrastructure layer)
   - Enable RDS/Cloud SQL encryption at rest
   - Protects against physical theft

2. **Application-Level Encryption** (Application layer)
   - Encrypt `extracted_text` field
   - Protects against database breach

3. **TLS/SSL for Data in Transit** (Network layer)
   - Already using HTTPS
   - Database connections over SSL

### Implementation Steps:

1. **Short-term (Easy):**
   ```bash
   # Enable cloud provider encryption
   # AWS RDS, Google Cloud SQL, or Azure
   ```

2. **Medium-term (Recommended):**
   ```python
   # Implement application-level encryption
   # For sensitive fields like extracted_text
   ```

3. **Long-term (Advanced):**
   ```bash
   # Implement key rotation
   # Set up HSM or secrets manager
   # Audit all encryption access
   ```

---

## Key Management

### Best Practices:

1. **Never hardcode keys in code**
   ```python
   # ❌ BAD
   KEY = "my-encryption-key-123"

   # ✅ GOOD
   KEY = os.getenv('ENCRYPTION_KEY')
   ```

2. **Use different keys for different environments**
   ```bash
   # Development
   ENCRYPTION_KEY=dev-key-abc123

   # Production
   ENCRYPTION_KEY=prod-key-xyz789
   ```

3. **Rotate keys regularly**
   - Schedule: Every 90 days minimum
   - Process: Re-encrypt data with new key
   - Audit: Log all key rotations

4. **Use a secrets manager:**
   - AWS Secrets Manager
   - HashiCorp Vault
   - Azure Key Vault
   - Google Secret Manager

---

## Testing Encryption

```python
# Test script: backend/tests/test_encryption.py
from app.utils.field_encryption import FieldEncryptor

def test_encryption():
    encryptor = FieldEncryptor()

    # Original text
    original = "John Smith, email: john@example.com"

    # Encrypt
    encrypted = encryptor.encrypt(original)
    print(f"Encrypted: {encrypted}")

    # Decrypt
    decrypted = encryptor.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")

    # Verify
    assert original == decrypted, "Encryption/decryption failed!"
    print("✅ Encryption test passed!")

if __name__ == "__main__":
    test_encryption()
```

---

## GDPR Compliance Checklist

- [ ] Enable database encryption at rest
- [ ] Implement application-level encryption for sensitive fields
- [ ] Use TLS/SSL for data in transit
- [ ] Implement key rotation policy
- [ ] Use secrets manager for key storage
- [ ] Document encryption methods
- [ ] Test encryption/decryption
- [ ] Train team on key management
- [ ] Include in disaster recovery plan

---

## Migration Plan

### If Adding Encryption to Existing Data:

```python
# Migration script: backend/migrations/encrypt_existing_data.py
from app.models import Contract
from app.database import SessionLocal
from app.utils.field_encryption import FieldEncryptor

def encrypt_existing_contracts():
    db = SessionLocal()
    encryptor = FieldEncryptor()

    contracts = db.query(Contract).all()

    for contract in contracts:
        if contract.extracted_text and not contract.extracted_text.startswith('gAAAAA'):  # Not already encrypted
            # Encrypt the text
            encrypted = encryptor.encrypt(contract.extracted_text)
            contract._extracted_text_encrypted = encrypted

    db.commit()
    print(f"✅ Encrypted {len(contracts)} contracts")

if __name__ == "__main__":
    encrypt_existing_contracts()
```

---

## Performance Impact

### Benchmarks:

| Method | Read Overhead | Write Overhead | Storage Overhead |
|--------|--------------|----------------|------------------|
| **No Encryption** | 0ms | 0ms | 0% |
| **Application-Level** | ~5ms | ~5ms | +33% (base64) |
| **PostgreSQL pgcrypto** | ~10ms | ~10ms | +33% (base64) |
| **TDE (LUKS)** | <1ms | <1ms | +0% |
| **Cloud Provider** | <1ms | <1ms | +0% |

**Recommendation:** Use TDE or Cloud Provider encryption for best performance with full security.

---

## Support & Resources

- PostgreSQL Encryption: https://www.postgresql.org/docs/current/encryption-options.html
- AWS RDS Encryption: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html
- Python Cryptography: https://cryptography.io/
- GDPR Article 32: https://gdpr-info.eu/art-32-gdpr/

---

**Last Updated:** November 15, 2025
**Next Review:** February 15, 2026
