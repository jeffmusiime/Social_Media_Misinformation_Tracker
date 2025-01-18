#!/usr/bin/env python3
import pandas as pd
import requests
import json
from datetime import datetime
import csv
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import re

class MisinformationTracker:
    def __init__(self):
        self.data = []
        self.network = nx.Graph()
        
    def collect_posts(self, keywords, platform="twitter", limit=100):
        """
        Simulate collecting posts containing specific keywords
        In real implementation, would use platform APIs
        """
        # Placeholder for API collection
        self.data = [{
            'timestamp': datetime.now().isoformat(),
            'platform': platform,
            'content': f"Sample post containing {keywords}",
            'user': f"user_{i}",
            'engagement': {'likes': i*10, 'shares': i*2},
            'links': [f"http://example{i}.com"],
            'hashtags': [f"#{keywords}", "#sample"]
        } for i in range(limit)]
        
    def analyze_network(self):
        """Analyze connection patterns between users sharing similar content"""
        # Build network graph
        for post in self.data:
            self.network.add_node(post['user'])
            # Connect users who share same hashtags
            for other_post in self.data:
                if post != other_post:
                    common_tags = set(post['hashtags']).intersection(other_post['hashtags'])
                    if common_tags:
                        self.network.add_edge(post['user'], other_post['user'])
        
        # Calculate network metrics
        centrality = nx.degree_centrality(self.network)
        communities = list(nx.community.greedy_modularity_communities(self.network))
        
        return {
            'central_nodes': sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10],
            'community_count': len(communities),
            'density': nx.density(self.network)
        }
    
    def identify_narratives(self):
        """Identify common narratives and themes"""
        all_content = ' '.join([post['content'] for post in self.data])
        words = re.findall(r'\w+', all_content.lower())
        word_freq = Counter(words).most_common(20)
        
        hashtags = [tag for post in self.data for tag in post['hashtags']]
        hashtag_freq = Counter(hashtags).most_common(10)
        
        return {
            'common_words': word_freq,
            'common_hashtags': hashtag_freq
        }
    
    def analyze_engagement(self):
        """Analyze engagement patterns"""
        df = pd.DataFrame(self.data)
        engagement_stats = {
            'total_likes': sum(p['engagement']['likes'] for p in self.data),
            'total_shares': sum(p['engagement']['shares'] for p in self.data),
            'avg_engagement': sum(p['engagement']['likes'] + p['engagement']['shares'] 
                                for p in self.data) / len(self.data)
        }
        return engagement_stats
    
    def generate_report(self):
        """Generate analysis report"""
        network_analysis = self.analyze_network()
        narrative_analysis = self.identify_narratives()
        engagement_analysis = self.analyze_engagement()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'data_points': len(self.data),
            'network_analysis': network_analysis,
            'narrative_analysis': narrative_analysis,
            'engagement_analysis': engagement_analysis
        }
        
        return report
    
    def visualize_network(self, output_file="network_visualization.png"):
        """Create network visualization"""
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.network)
        nx.draw(self.network, pos, 
                node_color='lightblue', 
                node_size=500, 
                with_labels=True,
                font_size=8)
        plt.title("Information Spread Network")
        plt.savefig(output_file)
        plt.close()

    def export_data(self, filename="misinfo_analysis.csv"):
        """Export analyzed data to CSV"""
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp', 'platform', 'content', 
                                                 'user', 'engagement', 'links', 'hashtags'])
            writer.writeheader()
            writer.writerows(self.data)

def main():
    # Initialize tracker
    tracker = MisinformationTracker()
    
    # Collect data
    tracker.collect_posts(keywords="election2024")
    
    # Generate and print report
    report = tracker.generate_report()
    print(json.dumps(report, indent=2))
    
    # Create visualizations
    tracker.visualize_network()
    
    # Export data
    tracker.export_data()

if __name__ == "__main__":
    main()
