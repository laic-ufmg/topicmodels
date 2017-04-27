# Methods for Expanding Short Text for Topic Modeling

Code related to the project to improve topic modeling for short text.

Here you can find the codes for DREX and COFE, both described in 

Paulo Bicalho, Marcelo Pita, Gabriel Pedrosa, Anisio Lacerda, Gisele L. Pappa, A general framework to expand short text for topic modeling, Information Sciences, Volume 393, July 2017, Pages 66-81, ISSN 0020-0255, http://doi.org/10.1016/j.ins.2017.02.007.
(http://www.sciencedirect.com/science/article/pii/S0020025517304206)

Paper Abstract: 
Short texts are everywhere in the Web, including messages posted in social media, status messages and blog comments, and uncovering the topics of this type of messages is crucial to a wide range of applications, e.g., context analysis and user characterization. Extracting topics from short text is challenging because of the dependence of conventional methods, such as Latent Dirichlet Allocation, in words co-occurrence, which in short text is rare and make these methods suffer from severe data sparsity. This paper proposes a general framework for topic modeling of short text by creating larger pseudo-document representations from the original documents. In the framework, document components (e.g., words or bigrams) are defined over a metric space, which provides information about the similarity between them. We present two simple, effective and efficient methods that specialize our general framework to create larger pseudo-documents. While the first method considers word co-occurrence to define the metric space, the second relies on distributed word vector representations. The pseudo-documents generated can be given as input to any topic modeling algorithm. Experiments run in seven datasets and compared against state-of-the-art methods for extracting topics by generating pseudo-documents or modifying current topic modeling methods for short text show the methods significantly improve results in terms of normalized pointwise mutual information. A classification task was also used to evaluate the quality of the topics in terms of document representation, where improvements in F1 varied from 1.5 to 15%.
Keywords: Topic modeling; Short text; Word vector representation; Pseudo-documents


