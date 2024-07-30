#ifndef SCANNER_H
#define SCANNER_H

#include <string>
#include <vector>
#include <map>
#include "Token.h"
#include "bashika.h"

class Scanner{
public:
    Scanner(const std::string &input_source){
      // source = input_source; 
      // the source() is an initializer list which helps with clarity in code
      // we have to use an initializer list because the source string is a const
      // which means it cannot be initialized as an empty string and then assigned a value (since the value has to be constant and unchanging
      // this also improves efficiency because using "source = input_source;" will initialize the source string to an empty string and then assign the value input_source to it which is 2 operations
      // using the initializer list is more efficient cuz its 1 operation
      source(input_source);
    }
    std::vector<Token> scanTokens(){
      while (!isAtEnd()){
        start = current;
        scanToken();
      }
    
      tokens.push_back(Token("\0", "", NULL, line));
    }

private:
    const std::string source;
    std::vector<Token> tokens;
    int start = 0;
    int current = 0;
    int line = 1;
    const std::map<std::string, TokenType> keywords = {
      {"and",    TokenType::AND},
      {"class",  TokenType::CLASS},
      {"else",   TokenType::ELSE},
      {"false",  TokenType::FALSE},
      {"for",    TokenType::FOR},
      {"fun",    TokenType::FUN},
      {"if",     TokenType::IF},
      {"nil",    TokenType::NIL},
      {"or",     TokenType::OR},
      {"print",  TokenType::PRINT},
      {"return", TokenType::RETURN},
      {"super",  TokenType::SUPER},
      {"this",   TokenType::THIS},
      {"true",   TokenType::TRUE},
      {"var",    TokenType::VAR},
      {"while",  TokenType::WHILE}
    };

    bool isatEnd(){
      return current >= source.length();
    }

    char advance(){
      // using .at() here because unsure about index being in bounds
      // could use the [] operator but that does not have bounds detection
      // .at() has slight overhead (due to bounds detection) but has error handling
      // the character in the source string at index current is used THEN current is incremented
      return source.at(current++);
    }

    void addToken(TokenType type){
      addToken(type, NULL); 
    }
    
    void addToken(TokenType type, std::variant<std::monostate, std::string, double> literal){
      // the .substr() function in C++ takes in the start index (inclusive) and the length of the substring we wish to extract
      // that is why we provided (current - start) as the second variable - the current index would also be incremented 1 past the desired end index as per the advance() method (the current variable gets incremented after using .at())
      std::string curr_lexeme = source.substr(start, (current - start));
      std::cout << "LEXEME IDENTIFIED - " << curr_lexeme << std::endl;
      tokens.push_back(Token(type, curr_lexeme, literal, line));
    }

    bool matchNext(char expected){
      if (isAtEnd()){
        return false;
      }
      // here we can use the [] operator instead of .at() because we previously checked if we were
      // at the end or not ensuring that value of current is a valid index
      if (source[current] == expected){
        current++;
        return true;
      }

      return false;
    }

    char peek(){
      if (isAtEnd()){
        return '\0';
      }
      return source[current];
    }

    char peekNext(){
      if ((current + 1) >= source.length()){
        return '\0';
      }
      
      return source[current+1];
    }
    
    bool isDigit(char c){
      return c >= '0' && c <='9';
    }

    bool isAlpha(char c){
      return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
    }

    bool isAlphaNumeric(char c){
      return isAlpha(c) || isDigit(c);
    }
    
    void addStringLiteral(){
      // essentially just advances to end of string or end of file
      while (peek() != '"' && !isAtEnd()){
        if (peek() == '\n'){
          line++;
        }
        advance();
      }
      if (isAtEnd()){
        error(line, "Unterminated string EOF.");
        return;
      }

      // now current is at the closing "
      advance();

      // std::vector<std::string> string_literal = {source.substr(start+1, (current - start))};
      std::variant<std::monostate, std::string, double> string_literal = source.substr(start+1, (current - start));
      addToken(STRING, string_literal);
    }

    void addNumberLiteral(){
      while (isDigit(peek())){
        advance();
      }

      // check if the . character detected is part of a number literal
      if (peek() == '.' && isDigit(peekNext())){
        // if so consume the . character as part of the number literal and continue
        advance();

        while (isDigit(peek())){
          advance();
        }
      }

      // using stod not atof because atof takes in char* and stod takes in std::string
      // both essentially take in a string and return a double
      addToken(NUMBER, std::stod(source.substr(start, (current-start))));
      
    }

    void addIdentifier(){
      while (isAlphaNumeric(peek())){
        advance();
      }

      std::string lexeme = source.substr(start, (current - end));
      // use .at() for bounds detection in keywords hashmap
      if (keywords.find(lexeme) != keywords.end()){
        TokenType type = keywords[lexeme];
      } else {
        TokenType type = IDENTIFIER;
      }

      addToken(type);
    }
    

    void scanToken(){
      char curr_character = advance();
      switch (curr_character){
        // OPERATORS
        case '(': addToken(LEFT_PAREN); break;
        case ')': addToken(RIGHT_PAREN); break;
        case '{': addToken(LEFT_BRACE); break;
        case '}': addToken(RIGHT_BRACE); break;
        case ',': addToken(COMMA); break;
        case '.': addToken(DOT); break;
        case '-': addToken(MINUS); break;
        case '+': addToken(PLUS); break;
        case ';': addToken(SEMICOLON); break;
        case '*': addToken(STAR); break; 
        case '!':
          // ternary operator checks if the next character is "="
          // if it is then it returns BANG_EQUAL (for "!=")
          // if isn't then it returns BANG (for "!")
          addToken(match('=') ? BANG_EQUAL : BANG);
          break;
        case '>':
          addToken(match('=') ? GREATER_EQUAL : GREATER);
          break;
        case '<':
          addToken(match('=') ? LESS_EQUAL : LESS);
          break;
        case '=':
          addToken(match('=') ? EQUAL_EQUAL : EQUAL);
          break;
        case '/':
          // this if is so we can check for comments
          // notice how the lexeme doesn't get added via addToken if its a comment
          if (match('/')){
            while (peek() != '\n' && !isAtEnd()){
              advance();
            } 
          }
          else {
            // this is for division
            addToken(SLASH);
          }
          break;

        // WHITESPACE & NEWLINES
        case ' ':
        case '\t':
        case '\r':
          break;

        case '\n':
          line++;
          break;

        // LITERALS
        case '"':
          addStringLiteral();
          break;

        // MAXIMAL MUNCH PROPERTY
        // maximual munch means that when two lexical grammar rules match a specfic lexeme or chunk of code, the grammar rule that matches the most characters, wins
        // so orchid matches both the identifier rule and the keyword rule
        // since the identifier rule matches "orchid" and the keyword rule matches "or" the identifier rule wins
        // so for the identifier and keyword rules we essentially assume we are reading in an identifier and just check if the identifier is a keyword or not so if we read in an identifier which is acutally just the keyword "or" for example we annotate it as a reserved word
        // however if we read in a lexeme and it doesnt match any keywords its read in as an identifier (assuming it doesnt match any other rules)
        default:
          if (isDigit(curr_character)){
            addNumberLiteral();
          }
          // Maximul Munch Rule for reserved words (keywords) and identifiers
          if (isAlpha(curr_character)){
            addIdentifier();
          }
          error(line, "Unexpected character");
          break;
      }
    }
};

#endif
