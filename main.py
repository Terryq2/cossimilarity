import calculation_class


# Program is currently calculating L2 result



#TODO: Testing has to be parametrized. Only parametrized the single function and did not amend the other functions so the other functions

#TODO Change the function to turn all to lower case except proper nouns

#TODO: Make main program more pretty


def print_box_with_message(width, height, message_lines):
    if height < 2 or width  < len(message_lines) + 2:
        print("Height must be at least 2 and width must be enough to fit the message.")
        return
    
    # Top border
    print("+" + "-" * (width - 2) + "+")
    
    # Calculate padding
    top_padding = (height - len(message_lines) - 2) // 2
    bottom_padding = height - len(message_lines) - top_padding - 2
    
    # Print top padding
    for _ in range(top_padding):
        print("|" + " " * (width - 2) + "|")
    
    # Print each line of the message
    for line in message_lines:
        line = line[:width-2]  # Truncate if the line is too long
        padding = (width - 2 - len(line)) // 2
        print("|" + " " * padding + line + " " * (width - 2 - len(line) - padding) + "|")
    
    # Print bottom padding
    for _ in range(bottom_padding):
        print("|" + " " * (width - 2) + "|")
    
    # Bottom border
    print("+" + "-" * (width - 2) + "+")


if __name__ == "__main__":

    position_of_word: int = 5
    position_of_word_class: int = 7
    position_of_part_of_speech: int = 9
    position_of_sentence_id: int = 3
    similarity_writeto_position: int = 8


    program = calculation_class.Calculations()
    
    #Collumn names must match the column names of the file for correctness.
    column_names : list[str] = ["Passage","WordNo","NewID","Sentence","WP","WordNoPunctuation","Word","WordClass","SimilarityWithPrevious", "PartOfSpeech"]


    column_names: list[str] = ["Passage","NewID","WordNo","Sentence","WordID","IDEnd","IDBegin","Word","WordWithPunctuation","WordNoPunctuation","WP","WL","WordClass","CosineSimilarity_Content_Sentence","PartOfSpeech"]
    # program.compute_similarities(position_of_sentence_id,position_of_word,position_of_word_class,position_of_part_of_speech,'L2 Stimuli.csv')
    program.compute_similarities(position_of_sentence_id,8,12,14, 'data.csv')
    program.write_similarity('data.csv','clean.txt',13, column_names)
    # program.write_similarity('L2 Stimuli.csv',"result_L2.csv",8, column_names)
    





