# nft-gen

Generate NFTs with combinations of various types of properties.

---

# Setup

1. Run `nft-gen.exe`.

    > This will generate some config files and create a folder named "Assets".


2. Create a subfolder for every type of property you want to include in the `Assets` folder.

    > This can be literally anything, with any names you want the properties to have.


3. Populate the subfolders with images of the corresponding property types.

    > For example, "Pirate Hat.png" in the subfolder "Hat".


4. Update `attributes.yaml`

    > Refer to the names of the subfolders as property types and the names of the individual files as the attributes (case sensitive).


5. Enter "generate" into the console

    > This will generate a new image based on your assets and configuration. Look for the result in the generated `out` folder.


# Tips

* Supply a number after "generate" to specify how many to generate (e.g., "generate 5").


* Use the shorthand "g" instead of "generate".
