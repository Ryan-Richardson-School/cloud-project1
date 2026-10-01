import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


#setup data

df = pd.read_csv('All_Diets.csv')

df['Protein(g)'] = df['Protein(g)'].fillna(df['Protein(g)'].mean())
df['Carbs(g)'] = df['Carbs(g)'].fillna(df['Carbs(g)'].mean())
df['Fat(g)'] = df['Fat(g)'].fillna(df['Fat(g)'].mean())

#calcs
avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)

highest_protein_diet = avg_macros['Protein(g)'].idxmax()

common_cuisines = df.groupby('Diet_type')['Cuisine_type'].agg(
	lambda x: x.value_counts().idxmax())

df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']

#print statements
print("Average macronutierents by Diet Type:")
print(avg_macros)

print("\nTop 5 Protein-Rich Recipes for Each Diet Type:")
print(top_protein)

print("\nDiet Type with Highest Protein Content:")
print(highest_protein_diet)

print("\nMost Common Cuisine for Each Diet Type:")
print(common_cuisines)

print("\Dataset with New Ratio Metrics:")
print(df[['Diet_type', 'Recipe_name', 'Protein_to_Carbs_ratio', 'Carbs_to_Fat_ratio']].head())



sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'])
plt.title('Average Protein by Diet Type')
plt.ylabel('Average Protein (g)')
plt.savefig('average_protein_by_diet.png')
plt.close()

#heatmap

plt.figure(figsize=(8, 5))
sns.heatmap(avg_macros, annot=True, fmt='.2f')
plt.title('Average Macronutrients Content by Diet Type')
plt.savefig('macronutrient_heatmap.png')
plt.close()

#scatterplot
plt.figure(figsize=(10, 6))
sns.scatterplot(
	data=top_protein,
	x='Cuisine_type',
	y='Protein(g)',
	hue='Diet_type')

plt.title('Top 5 Protein-Rich Recipes Across Cuisines')
plt.xlabel('Cuisine Type')
plt.ylabel('Protein (g)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('top_protein_scatterplot.png')
plt.close()
