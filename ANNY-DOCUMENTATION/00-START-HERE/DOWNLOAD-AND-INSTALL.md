# ANNY: Download & Install Guide

ANNY is a distributable governed runtime. Each customer installs the same ANNY product while retaining an independent GitHub identity, repository scope, and durable instance state.

## 1. Download

Use the official releases of `GRECOITALICO/ANNY`. Release artifacts are versioned and accompanied by a SHA-256 digest.

## 2. Verify the artifact

After downloading the ZIP, run:

```bash
sha256sum ANNY-vX.Y.Z.zip
```

Compare the result with the digest published for that release.

## 3. Create your own GitHub repository

Create a private repository in your own GitHub account, for example:

```text
YOUR-ACCOUNT/ANNY
```

Do not grant ANNY access to repositories outside the scope you intend to authorize.

## 4. Install the public distribution

Extract the release and publish the ANNY product code to your own repository:

```bash
unzip ANNY-vX.Y.Z.zip -d anny-install
cd anny-install
git init
git branch -M main
git remote add origin https://github.com/YOUR-ACCOUNT/ANNY.git
git add .
git commit -m "Initial ANNY installation"
git push -u origin main
```

## 5. Connect GitHub to your AI client

Authenticate the GitHub account you intend ANNY to use. The authenticated GitHub principal is the source of repository identity and scope. A caller-supplied login, owner, or user id is not an authorization source.

## 6. Start ANNY

Open a new ChatGPT conversation and ask ANNY to initialize the repository. ANNY should first inspect the durable state, identify the authenticated principal, and determine whether the repository is uninitialized.

## 7. First bootstrap

A new instance begins unactivated. Genesis/bootstrapping creates the local organizational state required by the product. It must not import another customer's state or CONRRAD's internal organizational state.

## 8. Repository Fabric

ANNY uses a public Repository Fabric client/contract boundary. Repository Fabric itself is shared infrastructure operated outside this public repository. The public distribution must not contain the private Fabric implementation.

## 9. Persistence and reconstruction

Operational state, missions, decisions, messages, and evidence are persisted durably according to the ANNY contracts so a later process can reconstruct context without conversational memory.

## 10. Important boundary

`ANNY` is the product. `GitHub` supplies the customer's authenticated identity and repository ownership/scope. `Repository Fabric` is shared infrastructure. `CONRRAD` remains the internal certification and infrastructure environment.

See also:

- `ANNY-DOCUMENTATION/PUBLIC-PRODUCT-BOUNDARY.md`
- `ANNY-DOCUMENTATION/PUBLIC-CERTIFICATION-BASELINE.md`
