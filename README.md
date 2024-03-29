## Usage

To get started with WikiGenGPT and generate your fictional Wikipedia articles, follow these steps:

1. **Set Up the Environment:**
   - Ensure you have Python 3.6 or later installed on your machine.
   - Clone the repository to your local environment:
     ```
     git clone https://github.com/mrconter1/WikiGenGPT
     ```
   - Navigate into the cloned directory:
     ```
     cd WikiGenGPT
     ```
   - Install the required dependencies:
     ```
     pip3 install -r requirements.txt
     ```
   
2. **API Key Configuration:**
   - Obtain your GPT-4 API key from OpenAI.
   - Open the `wikigengpt.py` file in a text editor.
   - Locate the line that says `openai.api_key = "YOUR_API_KEY"` and replace `YOUR_API_KEY` with your actual GPT-4 API key.

3. **Generate Articles:**
   - Run the script with the command:
     ```
     python3 wikigengpt.py
     ```
	or for custom concept
     ```
     python3 wikigengpt.py --user_concept "Fictional Concept"
     ```
   - When prompted, enter the subject or title for the fictional Wikipedia article you want to generate.
   - The script will process your request and output a fictional Wikipedia-style article.

4. **Navigation and Exploration:**
   - The generated article includes clickable hyperlinks. Click on these links to navigate to other related fictional articles.
   - Feel free to explore the vast universe of content created by WikiGenGPT.

5. **Customization:**
   - You can customize the script to change the structure of the articles or the way they are generated by editing the `wikigengpt.py` file.

Remember to use this tool responsibly and be aware that the content is fictional and generated for entertainment purposes only.

## Contributing

Contributions to WikiGenGPT are welcome! If you have suggestions for improvements or new features, feel free to fork the repository, make your changes, and submit a pull request.

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository, and the maintainers will help you out.

Happy exploring in the fictional world of WikiGenGPT!
