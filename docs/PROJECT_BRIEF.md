# EcoSort AI — Project Brief

## Project Title
EcoSort AI: An Agentic AI Assistant for Intelligent Waste Segregation and Responsible Disposal

## Primary SDG
SDG 12 – Responsible Consumption and Production

## Problem Statement
How might we use AI to help people correctly identify, segregate, and responsibly handle everyday waste so that waste management can become more sustainable?

## Target Users
- Students
- Households
- Office and campus users
- General citizens

## Proposed Solution
EcoSort AI accepts a waste description or an image. The system analyzes the item, classifies it into a defined waste category, retrieves relevant guidance from a small knowledge base, and generates a practical recommendation.

The system is designed to avoid unsupported disposal claims. When information is insufficient, it can return an uncertain result rather than forcing a category.

## Waste Categories
1. Organic / Food Waste
2. Paper / Cardboard
3. Plastic
4. Glass
5. Metal
6. E-Waste
7. Batteries
8. Sanitary / Hygiene Waste
9. Hazardous / Chemical Waste
10. Mixed / Unknown

## AI and Technical Components
- IBM watsonx.ai
- IBM Granite text model
- IBM Granite Vision model where available
- LangGraph workflow
- Retrieval-augmented guidance
- TF-IDF retrieval using scikit-learn
- Streamlit interface

## Workflow
User Input → Image/Text Understanding → Classification → RAG Retrieval → Conditional Routing → Recommendation → User Interface

## Responsible Design
### Fairness
Use defined categories and avoid assumptions about users or locations that are not supported by the input.

### Transparency
Show the classification and retrieved guidance used to support the recommendation.

### Ethics and Safety
Do not provide instructions for unsafe handling of hazardous materials, batteries, or broken items. Avoid unsupported claims.

### Privacy
The prototype does not require names, phone numbers, email addresses, or other personal information. Uploaded images are used for the analysis flow and are not intentionally stored by the application.

## Limitations
- Local waste rules differ across regions.
- The prototype is not an authority on municipal collection schedules.
- Image classification depends on image quality and model availability.
- Retrieved guidance is limited to the project's curated knowledge base.

## Future Development
- Location-aware municipal guidance
- Broader waste-item coverage
- More detailed evaluation with a labeled test set
- Additional multilingual support
- Collection-center discovery using verified location data
