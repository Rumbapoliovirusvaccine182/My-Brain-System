# Task: Deploy Migration Plan
# Trigger: User says "Deploy Plan"

# Context:
The user has approved the `Migration_Plan.md`. You are now authorized to restructure the file system.

# Steps:
1. **Read Plan**: Parse `Migration_Plan.md` to understand the mapping.
2. **Create Folders**: Create the new directories in `10_Garden/`.
3. **Move Files**: Move files to their new destinations as per the plan.
4. **Cleanup**: Delete any empty directories left behind in `10_Garden/`.
5. **Update Rules (CRITICAL)**:
   - Rewrite `.agent/taxonomy.md` if category definitions changed.
   - Update it with the new categories and their definitions found in the Plan.
   - This ensures future `Ingest` tasks follow this new structure.
6. **Generate Indices**: 
   - Execute `.agent/tasks/generate_indices.md` for each category.
   - Create `主題索引.md` in each non-empty folder.
7. **Check Category Sizes (NEW)**:
   - Execute `.agent/tasks/subdivide.md` to analyze category sizes.
   - If any category > 20 notes, propose subdivision.
   - Present subdivision plan to user for approval.

# Final Output:
- Delete `Migration_Plan.md`.
- Report: "✅ Garden Restructured. Taxonomy rules updated."
- If subdivisions recommended: "🔍 Subdivision Recommended: [Category] → See [Category]_Subdivision_Plan.md"