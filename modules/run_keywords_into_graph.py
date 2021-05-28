import sys
import os
sys.path.insert(0, 'backend processing')
import keywords_into_graph as kwg

def main():
    keyword = 'COVID-19'
    kwg.turn_keywords_into_graph(keyword)

if __name__ == '__main__':
    main()
